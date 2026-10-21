"""Regression checks for the data-quality-frameworks skill (splitter corruption, GX 0.x APIs)."""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest
import yaml

SKILL = (
    Path(__file__).resolve().parents[2]
    / "plugins"
    / "data-engineering"
    / "skills"
    / "data-quality-frameworks"
)
FILES = [SKILL / "SKILL.md", SKILL / "references" / "details.md"]
IDS = ["SKILL.md", "details.md"]

# Calls and imports that only exist in Great Expectations 0.x.
GX_0X = [
    r"great_expectations init",
    r"great_expectations datasource",
    r"run_checkpoint\(",
    r"add_expectation_suite\(",
    r"ExpectationConfiguration",
    r"expectation_type",
    r"class_name: Checkpoint",
    r"gx\.DataContext\b",
    r"StoreEvaluationParametersAction",
]


def _blocks(path: Path, lang: str) -> list[str]:
    return re.findall(rf"^```{lang}\n(.*?)^```", path.read_text(), re.S | re.M)


@pytest.mark.parametrize("path", FILES, ids=IDS)
def test_fences_are_balanced(path: Path) -> None:
    fences = re.findall(r"^```", path.read_text(), re.M)
    assert len(fences) % 2 == 0


@pytest.mark.parametrize("path", FILES, ids=IDS)
def test_no_splitter_fragment(path: Path) -> None:
    text = path.read_text()
    assert "{total_passed}" not in text
    # Every heading is outside a code block, so none can contain code punctuation.
    prose = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)
    for heading in re.findall(r"^#+ .*$", prose, re.M):
        assert not re.search(r"[{}]|\"\)", heading), heading


@pytest.mark.parametrize("path", FILES, ids=IDS)
def test_gx_examples_use_1x_api(path: Path) -> None:
    # Prose may name 0.x calls to warn against them; code must not use them.
    text = "\n".join(re.findall(r"^```\w*\n(.*?)^```", path.read_text(), re.S | re.M))
    for pattern in GX_0X:
        assert not re.search(pattern, text), pattern


@pytest.mark.parametrize("path", FILES, ids=IDS)
def test_code_blocks_parse(path: Path) -> None:
    for block in _blocks(path, "python"):
        ast.parse(block)
    for block in _blocks(path, "yaml"):
        yaml.safe_load(block)


def test_skill_has_enforced_dbt_contract() -> None:
    models = [yaml.safe_load(b) for b in _blocks(SKILL / "SKILL.md", "yaml")]
    contracts = [
        m
        for doc in models
        if isinstance(doc, dict)
        for m in doc.get("models", [])
        if m.get("config", {}).get("contract", {}).get("enforced") is True
    ]
    assert contracts
    for model in contracts:
        assert all("data_type" in c for c in model["columns"])


def test_skill_has_procedure_and_last_verified() -> None:
    text = (SKILL / "SKILL.md").read_text()
    assert "## Procedure" in text
    assert re.search(r"^last_verified: \d{4}-\d{2}-\d{2}$", text, re.M)
