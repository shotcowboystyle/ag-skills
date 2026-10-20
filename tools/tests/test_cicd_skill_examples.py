"""Regression checks for the CI examples in the cicd-automation secrets and pipeline skills."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

SKILLS = Path(__file__).resolve().parents[2] / "plugins" / "cicd-automation" / "skills"
NAMES = ["secrets-management", "github-actions-templates", "gitlab-ci-patterns"]


def _text(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text()


def _yaml_blocks(name: str) -> list[str]:
    return re.findall(r"```yaml\n(.*?)```", _text(name), re.S)


@pytest.mark.parametrize("name", NAMES)
def test_actions_are_sha_pinned(name: str) -> None:
    refs = re.findall(r"uses:\s*([\w.-]+/[\w./-]+)@(\S+)", _text(name))
    loose = [f"{a}@{r}" for a, r in refs if not re.fullmatch(r"[0-9a-f]{40}", r)]
    assert not loose


@pytest.mark.parametrize("name", NAMES)
def test_no_static_cloud_or_vault_credentials(name: str) -> None:
    text = _text(name)
    assert "aws-access-key-id" not in text
    assert "VAULT_TOKEN: ${{" not in text
    assert "token: ${{ secrets.VAULT" not in text
    assert not re.search(r"export VAULT_TOKEN=['\"]?\$VAULT_TOKEN", text)


@pytest.mark.parametrize("name", NAMES)
def test_no_example_echoes_a_secret(name: str) -> None:
    code = "\n".join(re.findall(r"```\w*\n(.*?)```", _text(name), re.S))
    assert not re.search(r"echo [^|\n]*\$\{?(API_KEY|DB_PASSWORD|SECRET|DATABASE_URL)", code)


def test_trufflehog_cli_calls_fail_on_findings() -> None:
    calls = re.findall(
        r"^\s*(?:- )?(?:trufflehog|git file:///).*$", _text("secrets-management"), re.M
    )
    assert calls
    assert all("--fail" in c for c in calls), calls


@pytest.mark.parametrize("name", NAMES)
def test_blocking_scans_are_not_allowed_to_fail(name: str) -> None:
    for block in _yaml_blocks(name):
        if "--exit-code 1" in block or "--fail" in block:
            assert "allow_failure: true" not in block


def test_github_workflows_default_to_read_only_permissions() -> None:
    workflows = [
        b for b in _yaml_blocks("github-actions-templates") if re.search(r"^jobs:", b, re.M)
    ]
    assert workflows
    for wf in workflows:
        assert re.search(r"^permissions:\n  contents: read$", wf, re.M), wf.splitlines()[0]


def test_github_deploy_jobs_use_an_environment() -> None:
    for block in _yaml_blocks("github-actions-templates"):
        if "kubectl apply" in block:
            assert "environment:" in block


def test_gitlab_examples_run_as_written() -> None:
    text = _text("gitlab-ci-patterns")
    assert not re.search(r"^\s*(only|except):", text, re.M)
    assert not re.search(r"docker login[^\n]*\s-p\s", text)
    assert "bitnami/" not in re.sub(r"#.*", "", text)
    # A top-level before_script leaks into every job.
    for block in _yaml_blocks("gitlab-ci-patterns"):
        assert not re.search(r"^before_script:", block, re.M)
    # Tool images whose entrypoint is the tool need it cleared for `script:` to run.
    for image in re.findall(r"image:\s*\n\s*name:\s*(\S+)\n(\s*\S.*)", text):
        if image[0].startswith(("hashicorp/", "aquasec/", "trufflesecurity/", "alpine/k8s")):
            assert 'entrypoint: [""]' in image[1], image[0]
    for bare in re.findall(r"image:\s*((?:hashicorp|aquasec)/\S+)", text):
        pytest.fail(f"{bare} needs entrypoint override")


@pytest.mark.parametrize("name", NAMES)
def test_last_verified_is_set(name: str) -> None:
    assert re.search(r"^last_verified: \d{4}-\d{2}-\d{2}$", _text(name), re.M)
