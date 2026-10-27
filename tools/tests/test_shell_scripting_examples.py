"""Regression checks for the shell-scripting plugin's version checks and examples."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[2] / "plugins" / "shell-scripting"
BASH_PRO = PLUGIN / "agents" / "bash-pro.md"
POSIX_PRO = PLUGIN / "agents" / "posix-shell-pro.md"
DEFENSIVE = PLUGIN / "skills" / "bash-defensive-patterns" / "SKILL.md"
SHELLCHECK = PLUGIN / "skills" / "shellcheck-configuration" / "SKILL.md"
BATS = PLUGIN / "skills" / "bats-testing-patterns"


def _blocks(path: Path, lang: str) -> list[str]:
    return re.findall(rf"```{lang}\n(.*?)```", path.read_text(), re.S)


def _version_check(path: Path) -> str:
    line = re.search(r"^bash_at_least\(\) \{.*\}$", path.read_text(), re.M)
    assert line, path
    return line.group(0)


def _all_text() -> str:
    return "\n".join(p.read_text() for p in PLUGIN.rglob("*.md"))


@pytest.mark.parametrize(
    ("major", "minor", "expected"),
    [(3, 2, 1), (4, 3, 1), (4, 4, 0), (5, 0, 0), (5, 3, 0), (6, 0, 0)],
)
@pytest.mark.parametrize("path", [BASH_PRO, DEFENSIVE], ids=["bash-pro", "skeleton"])
def test_bash_at_least_4_4(path: Path, major: int, minor: int, expected: int) -> None:
    # BASH_VERSINFO is readonly, so run the documented check against a stand-in array.
    func = _version_check(path).replace("BASH_VERSINFO", "V")
    script = f"V=({major} {minor}); {func}; bash_at_least 4 4"
    assert subprocess.run(["bash", "-c", script]).returncode == expected


def test_no_minor_only_version_checks() -> None:
    text = _all_text()
    assert not re.search(r"BASH_VERSINFO\[0\]\s*>=\s*\d+\s*&&\s*BASH_VERSINFO\[1\]", text)
    assert not re.search(r"BASH_VERSINFO\[0\]\}\s*-ge\s*\d+\s*&&\s*\$\{BASH_VERSINFO\[1\]", text)


def test_corrected_facts_and_links() -> None:
    text = _all_text()
    for stale in ("CodeQL", "bash-hackers.org", "PEASS-ng", "skip_if", "9699919799"):
        assert stale not in text, stale
    assert "No `declare`, `typeset`, or `readonly`" not in text
    assert "no `pipefail` in POSIX" not in text
    assert "`set -o pipefail` (bash-specific)" not in text
    bash_pro = BASH_PRO.read_text()
    assert re.search(r"\| 5\.0 \|[^\n]*EPOCHREALTIME", bash_pro)
    assert re.search(r"\| 5\.1 \|[^\n]*\$\{var@U\}", bash_pro)


@pytest.mark.parametrize("path", [BASH_PRO, POSIX_PRO])
def test_agents_have_trigger_and_tools(path: Path) -> None:
    front = path.read_text().split("---")[1]
    assert re.search(r"^description: .*Use when ", front, re.M)
    assert re.search(r"^tools: ", front, re.M)


def test_bats_examples_use_bats_temp_dirs() -> None:
    for path in (BATS / "SKILL.md", BATS / "references" / "details.md"):
        text = path.read_text()
        assert not re.search(r"\$\{?TMPDIR\b", text), path
    assert "$BATS_TEST_TMPDIR" in (BATS / "SKILL.md").read_text()


@pytest.fixture
def skeleton(tmp_path: Path) -> Path:
    script = tmp_path / "archive-dir.sh"
    script.write_text(_blocks(DEFENSIVE, "bash")[0])
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.txt").write_text("hi\n")
    (tmp_path / "dst").mkdir()
    return script


def _run(*args: str | Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(a) for a in args], capture_output=True, text=True)


def test_skeleton_runs(skeleton: Path) -> None:
    src, dst = skeleton.parent / "src", skeleton.parent / "dst"
    assert _run("bash", "-n", skeleton).returncode == 0
    dry = _run("bash", skeleton, "-n", src, dst)
    assert dry.returncode == 0 and "would run: tar" in dry.stdout
    assert not list(dst.iterdir())
    assert _run("bash", skeleton, src, dst).returncode == 0
    assert len(list(dst.glob("src-*.tar.gz"))) == 1
    assert _run("bash", skeleton).returncode == 2
    assert _run("bash", skeleton, "-x", src, dst).returncode == 2
    missing = _run("bash", skeleton, skeleton.parent / "nope", dst)
    assert missing.returncode == 1 and "not a directory" in missing.stderr


@pytest.mark.skipif(not Path("/bin/bash").exists(), reason="no /bin/bash")
def test_skeleton_refuses_old_bash(skeleton: Path) -> None:
    probe = _run("/bin/bash", "-c", "echo ${BASH_VERSINFO[0]}${BASH_VERSINFO[1]}")
    if int(probe.stdout) >= 44:
        pytest.skip("/bin/bash is 4.4 or newer")
    old = _run("/bin/bash", skeleton, skeleton.parent / "src", skeleton.parent / "dst")
    assert old.returncode == 1 and "needs bash >= 4.4" in old.stderr


@pytest.mark.skipif(not shutil.which("shellcheck"), reason="shellcheck not installed")
def test_skeleton_and_shellcheckrc_are_clean(skeleton: Path) -> None:
    (skeleton.parent / ".shellcheckrc").write_text(_blocks(SHELLCHECK, "ini")[0])
    result = _run("shellcheck", skeleton)
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize("shell", ["sh", "dash"])
def test_posix_patterns_run(shell: str) -> None:
    if not shutil.which(shell):
        pytest.skip(f"{shell} not installed")
    split, read_list = _blocks(POSIX_PRO, "sh")[1:3]
    assert _run(shell, "-c", split).stdout == "[a]\n[b c]\n[*]\n"
    assert _run(shell, "-c", read_list).stdout.endswith("count=2\n")
