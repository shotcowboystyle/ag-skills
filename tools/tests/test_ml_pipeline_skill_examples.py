"""Regression checks for the ml-pipeline-workflow skill (missing files, fake skills, placeholders)."""

from __future__ import annotations

import ast
import re
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2] / "plugins" / "machine-learning-ops"
SKILL = PLUGIN / "skills" / "ml-pipeline-workflow"
DAG = SKILL / "assets" / "ml_pipeline_dag.py"
GATE = ["MIN_ROC_AUC", "MIN_RECALL", "MAX_AUC_DROP"]


def _text() -> str:
    return (SKILL / "SKILL.md").read_text()


def test_referenced_files_exist() -> None:
    paths = re.findall(r"`((?:references|assets)/[^`]+)`", _text())
    assert paths
    for rel in paths:
        assert (SKILL / rel).is_file(), rel


def test_skill_links_resolve() -> None:
    for target in re.findall(r"\]\((\.\.[^)]+)\)", _text()):
        assert (SKILL / target).resolve().is_file(), target


def test_dag_asset_defines_gate_thresholds() -> None:
    tree = ast.parse(DAG.read_text())
    consts = {
        t.id: node.value.value
        for node in tree.body
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant)
        for t in node.targets
        if isinstance(t, ast.Name)
    }
    for name in GATE:
        assert isinstance(consts.get(name), float), name
        # SKILL.md shows the same values as the runnable asset.
        shown = re.search(rf"^{name} = ([\d.]+)", _text(), re.MULTILINE)
        assert shown and float(shown[1]) == consts[name], name


def test_code_blocks_are_not_comment_only() -> None:
    for block in re.findall(r"^```\w*\n(.*?)^```", _text(), re.DOTALL | re.MULTILINE):
        lines = [ln for ln in block.splitlines() if ln.strip()]
        assert any(not ln.lstrip().startswith("#") for ln in lines), block


def test_command_loads_skill() -> None:
    command = (PLUGIN / "commands" / "ml-pipeline.md").read_text()
    assert "Load the `ml-pipeline-workflow` skill" in command
