"""Regression checks for the skills repaired after the SKILL.md splitter (ticket 17)."""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

import pytest
import yaml

from tools.doc_gardener import Report, check_split_corruption

PLUGINS = Path(__file__).resolve().parents[2] / "plugins"
CHANGELOG = PLUGINS / "documentation-generation" / "skills" / "changelog-automation"
CHANGELOG_FILES = [CHANGELOG / "SKILL.md", CHANGELOG / "references" / "details.md"]
DESIGN_OPS = PLUGINS / "design-ops" / "skills"
HEADING = re.compile(r"^(#{1,6}) ")


def _blocks(path: Path, lang: str) -> list[str]:
    return re.findall(rf"^```{lang}\n(.*?)^```", path.read_text(), re.S | re.M)


def _changelog_blocks(lang: str) -> list[str]:
    return [b for p in CHANGELOG_FILES for b in _blocks(p, lang)]


def test_tree_has_no_split_corruption() -> None:
    report = Report()
    check_split_corruption(report)
    assert [f"{f.path}:{f.line}" for f in report.findings] == []


@pytest.mark.parametrize("path", CHANGELOG_FILES, ids=["SKILL.md", "details.md"])
def test_changelog_drops_standard_version_and_manual_edit_ban(path: Path) -> None:
    text = path.read_text()
    assert "Don't manual edit" not in text
    # standard-version may only be named as the thing to migrate away from.
    for line in text.splitlines():
        if "standard-version" in line:
            assert re.search(r"deprecated|migrat|replac|Remove", line, re.I), line


def test_changelog_has_no_unconfirmed_push() -> None:
    for path in CHANGELOG_FILES:
        assert not re.search(r"\bgit\s+push\b", path.read_text())


def test_changelog_releases_are_drafts() -> None:
    configs = [json.loads(b) for b in _changelog_blocks("json") if '"release-type"' in b]
    assert configs and all(c["draft"] is True for c in configs)
    gh_release = [line for b in _changelog_blocks("yaml") for line in b.splitlines() if "gh release create" in line]
    assert gh_release and all("--draft" in line for line in gh_release)


def test_changelog_examples_parse() -> None:
    for block in _changelog_blocks("yaml"):
        yaml.safe_load(block)
    for block in _changelog_blocks("json"):
        json.loads(block)
    cliff = [tomllib.loads(b) for b in _changelog_blocks("toml")]
    assert cliff and cliff[0]["git"]["conventional_commits"] is True


def test_changelog_actions_pinned_to_sha() -> None:
    uses = re.findall(r"uses: (\S+)", "\n".join(_changelog_blocks("yaml")))
    assert uses and all(re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", u) for u in uses), uses


@pytest.mark.parametrize("skill", ["icon-illustration-systems", "screen-flow-patterns", "page-composition-engine"])
def test_design_ops_skill_has_no_empty_sections(skill: str) -> None:
    """A heading followed straight by a same-or-higher heading is splitter residue."""
    lines = [line for line in (DESIGN_OPS / skill / "SKILL.md").read_text().splitlines() if line.strip()]
    for here, nxt in zip(lines, lines[1:]):
        a, b = HEADING.match(here), HEADING.match(nxt)
        if a and b:
            assert len(b.group(1)) > len(a.group(1)), f"empty section: {here!r}"


def test_page_composition_uses_no_undefined_block_ids() -> None:
    text = (DESIGN_OPS / "page-composition-engine" / "SKILL.md").read_text()
    ids = re.findall(r"\b(?:NAV|HERO|PROOF|FEAT|STATS|CTA|PRICE|FAQ|FOOTER|DASH|CONTENT|FORM|TEAM)-\d\d\b", text)
    assert ids == []
