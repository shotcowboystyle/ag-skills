"""Regression checks for the documentation-generation and conductor plugins."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

PLUGINS = Path(__file__).resolve().parents[2] / "plugins"
DOCS = PLUGINS / "documentation-generation"
CONDUCTOR = PLUGINS / "conductor"
OPENAPI = DOCS / "skills" / "openapi-spec-generation"
OPENAPI_FILES = [
    OPENAPI / "SKILL.md",
    OPENAPI / "references" / "details.md",
    OPENAPI / "references" / "code-first-and-tooling.md",
    DOCS / "commands" / "doc-generate.md",
]
CONDUCTOR_SKILLS = ["context-driven-development", "track-management", "workflow-patterns"]


def _blocks(path: Path, lang: str) -> list[str]:
    return re.findall(rf"^```{lang}\n(.*?)^```", path.read_text(), re.S | re.M)


def _frontmatter(path: Path) -> dict:
    return yaml.safe_load(path.read_text().split("---")[1])


def _keys(node: object) -> set[str]:
    if isinstance(node, dict):
        return set(node) | {k for v in node.values() for k in _keys(v)}
    if isinstance(node, list):
        return {k for v in node for k in _keys(v)}
    return set()


@pytest.mark.parametrize("path", OPENAPI_FILES, ids=lambda p: p.name)
def test_openapi_examples_are_3_1(path: Path) -> None:
    for block in _blocks(path, "yaml"):
        if "${" in block:  # doc-generate's template has shell-style placeholders
            block = re.sub(r"\$\{\w+\}", "x", block)
        doc = yaml.safe_load(block)
        assert "nullable" not in _keys(doc), "3.1 drops nullable; use type: [T, 'null']"
        if isinstance(doc, dict) and "openapi" in doc:
            assert str(doc["openapi"]).startswith("3.1"), doc["openapi"]


def test_openapi_skill_gives_lint_commands() -> None:
    skill = (OPENAPI / "SKILL.md").read_text()
    assert "## Procedure" in skill
    assert "npx @redocly/cli@2 lint" in skill
    assert "npx @stoplight/spectral-cli@6 lint" in skill
    assert re.match(r"\d{4}-\d{2}-\d{2}$", str(_frontmatter(OPENAPI / "SKILL.md")["last_verified"]))


def test_spectral_ruleset_uses_real_rule_names() -> None:
    ruleset = yaml.safe_load(
        _blocks(OPENAPI / "references" / "code-first-and-tooling.md", "yaml")[0]
    )
    assert ruleset["extends"] == ["spectral:oas"]
    assert "oas3-operation-security-defined" in ruleset["rules"]
    assert "operation-security-defined" not in ruleset["rules"]


@pytest.mark.parametrize("path", sorted((DOCS / "agents").glob("*.md")), ids=lambda p: p.stem)
def test_doc_agents_ask_for_no_unmeasured_numbers(path: Path) -> None:
    # Any mention of benchmarks must come with the "measured only" rule, in the same paragraph.
    for para in re.split(r"\n(?:\s*\n|\s*[-\d])", path.read_text()):
        if re.search(r"(?i)benchmark|rate limits and performance", para):
            assert re.search(r"(?i)measure", para), para


def test_reference_builder_on_sonnet_with_agent_shape() -> None:
    path = DOCS / "agents" / "reference-builder.md"
    meta, body = _frontmatter(path), path.read_text()
    assert meta["model"] == "sonnet"
    assert meta["tools"]
    for heading in ("## Input", "## Procedure", "## Output", "## Escalation"):
        assert heading in body, heading
    assert "needs measurement" in body
    assert "## Core Capabilities" not in body


def test_mermaid_expert_renders_and_knows_current_types() -> None:
    path = DOCS / "agents" / "mermaid-expert.md"
    body = path.read_text()
    assert _frontmatter(path)["tools"]
    assert "mmdc" in body
    for keyword in (
        "mindmap",
        "sankey",
        "xychart",
        "architecture-beta",
        "block",
        "C4Context",
        "kanban",
    ):
        assert f"`{keyword}`" in body, keyword


def test_adr_lifecycle_branches_from_accepted() -> None:
    skill = DOCS / "skills" / "architecture-decision-records" / "SKILL.md"
    diagram = next(b for b in _blocks(skill, "mermaid") if "stateDiagram" in b)
    for edge in (
        "Proposed --> Accepted",
        "Proposed --> Rejected",
        "Accepted --> Deprecated",
        "Accepted --> Superseded",
    ):
        assert edge in diagram, edge
    assert "Deprecated --> Superseded" not in diagram
    assert "Deprecated → Superseded" not in skill.read_text()


def test_validator_track_id_pattern_matches_command_ids() -> None:
    path = CONDUCTOR / "agents" / "conductor-validator.md"
    meta, body = _frontmatter(path), path.read_text()
    assert meta["model"] in {"haiku", "sonnet"}
    assert "<type>_<name>_<YYYYMMDD>" not in body
    pattern = re.search(r"grep -E '(.+?)'", body).group(1)
    ids = {
        m
        for cmd in (CONDUCTOR / "commands").glob("*.md")
        for m in re.findall(r"\b[a-z0-9-]+_\d{8}(?:_\d+)?\b", cmd.read_text())
    }
    assert {"user-auth_20250115", "user-auth_20250115_2"} <= ids
    for track_id in ids:
        assert re.fullmatch(pattern, track_id), track_id
    assert not re.fullmatch(pattern, "feature_user_auth_20250115")


def test_validator_runs_after_setup_and_before_implement() -> None:
    setup = (CONDUCTOR / "commands" / "setup.md").read_text()
    implement = (CONDUCTOR / "commands" / "implement.md").read_text()
    assert "subagent_type: conductor-validator" in setup
    assert "subagent_type: conductor-validator" in implement
    assert implement.index("conductor-validator") < implement.index("## Track Status Update")


@pytest.mark.parametrize("skill", CONDUCTOR_SKILLS)
def test_conductor_skills_carry_the_procedure(skill: str) -> None:
    text = (CONDUCTOR / "skills" / skill / "SKILL.md").read_text()
    assert "## Procedure" in text
    assert len(text.splitlines()) > 60
    assert not re.search(r"\*\*Task \d", text)
    details = (CONDUCTOR / "skills" / skill / "references" / "details.md").read_text()
    for moved in ("## TDD Task Lifecycle", "## Track ID Format", "## Session Continuity"):
        assert moved not in details, moved
    assert not re.search(r"\*\*Task \d", details)
