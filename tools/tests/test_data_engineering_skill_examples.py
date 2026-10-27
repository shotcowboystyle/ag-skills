"""Regression checks for the Airflow, dbt and Spark skills and the data-engineer agent."""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest
import yaml

PLUGIN = Path(__file__).resolve().parents[2] / "plugins" / "data-engineering"
SKILLS = ["airflow-dag-patterns", "dbt-transformation-patterns", "spark-optimization"]
FILES = [PLUGIN / "skills" / s / f for s in SKILLS for f in ("SKILL.md", "references/details.md")]
IDS = [f"{p.parts[-3] if p.name == 'details.md' else p.parts[-2]}/{p.name}" for p in FILES]

# Airflow 2 names that Airflow 3 removed or moved out of core.
AIRFLOW_2 = [
    r"from airflow\.decorators import",
    r"from airflow import DAG",
    r"from airflow\.operators\.",
    r"from airflow\.sensors\.",
    r"from airflow\.models import (DAG|Variable|DagBag)",
    r"from airflow\.datasets import",
    r"\bexecution_date\b",
    r"\bschedule_interval\b",
    r"include_examples",
]


def _blocks(path: Path, lang: str) -> list[str]:
    return re.findall(rf"^```{lang}\n(.*?)^```", path.read_text(), re.S | re.M)


def _frontmatter(path: Path) -> dict:
    return yaml.safe_load(path.read_text().split("---")[1])


@pytest.mark.parametrize("path", FILES, ids=IDS)
def test_code_blocks_parse(path: Path) -> None:
    assert len(re.findall(r"^```", path.read_text(), re.M)) % 2 == 0
    for block in _blocks(path, "python"):
        ast.parse(block)
    for block in _blocks(path, "yaml"):
        yaml.safe_load(block)


@pytest.mark.parametrize("name", ["SKILL.md", "references/details.md"])
def test_airflow_examples_use_airflow_3(name: str) -> None:
    code = "\n".join(_blocks(PLUGIN / "skills" / "airflow-dag-patterns" / name, "python"))
    assert "from airflow.sdk import" in code
    for pattern in AIRFLOW_2:
        assert not re.search(pattern, code), pattern


def test_airflow_quick_start_uses_taskflow() -> None:
    code = "\n".join(_blocks(PLUGIN / "skills" / "airflow-dag-patterns" / "SKILL.md", "python"))
    assert "@task" in code
    assert "PythonOperator" not in code


@pytest.mark.parametrize("name", ["SKILL.md", "references/details.md"])
def test_dbt_yaml_uses_current_syntax(name: str) -> None:
    path = PLUGIN / "skills" / "dbt-transformation-patterns" / name
    for block in _blocks(path, "yaml"):
        assert not re.search(r"^\s+tests:", block, re.M), "use data_tests:"
        assert not re.search(r"^\s+(loaded_at_field|freshness):", block, re.M) or "config:" in block
        # Generic tests with arguments nest them under `arguments:`.
        for test in ("relationships", "accepted_values", "dbt_utils.expression_is_true"):
            for m in re.finditer(rf"^(\s+)- {re.escape(test)}:\n\1    (\w+):", block, re.M):
                assert m.group(2) == "arguments", test


def test_dbt_layers_not_called_medallion() -> None:
    text = (PLUGIN / "skills" / "dbt-transformation-patterns" / "SKILL.md").read_text()
    assert not re.search(r"Model Layers \(Medallion", text)
    assert "don't\nmap one to one" in text or "don't map one to one" in text


@pytest.mark.parametrize("name", ["SKILL.md", "references/details.md"])
def test_spark_examples_skip_defaults_and_kryo(name: str) -> None:
    code = "\n".join(_blocks(PLUGIN / "skills" / "spark-optimization" / name, "python"))
    for default in (
        "spark.sql.adaptive.enabled",
        "spark.sql.adaptive.coalescePartitions.enabled",
        "spark.sql.adaptive.skewJoin.enabled",
        "KryoSerializer",
        "MEMORY_AND_DISK_SER",
    ):
        assert default not in code, default


def test_descriptions_name_tool_and_trigger_without_overlap() -> None:
    tools = {
        "airflow-dag-patterns": "Airflow",
        "dbt-transformation-patterns": "dbt",
        "spark-optimization": "Spark",
    }
    for skill, tool in tools.items():
        meta = _frontmatter(PLUGIN / "skills" / skill / "SKILL.md")
        assert meta["name"] == skill
        assert tool in meta["description"]
        assert "Use when" in meta["description"]
        assert re.match(r"\d{4}-\d{2}-\d{2}$", str(meta["last_verified"]))
        # Each description hands neighboring work to a sibling skill instead of claiming it.
        assert any(other in meta["description"] for other in set(tools) - {skill}), skill
        assert "## Procedure" in (PLUGIN / "skills" / skill / "SKILL.md").read_text()


def test_data_engineer_agent_shape() -> None:
    path = PLUGIN / "agents" / "data-engineer.md"
    meta = _frontmatter(path)
    body = path.read_text()
    assert meta["model"] == "sonnet"
    assert meta["tools"]
    for heading in ("## Input", "## Procedure", "## Output", "## Escalation"):
        assert heading in body, heading
    for skill in [*SKILLS, "data-quality-frameworks"]:
        assert f"`{skill}`" in body, skill
    assert "## Capabilities" not in body
    assert len(body.splitlines()) < 150
