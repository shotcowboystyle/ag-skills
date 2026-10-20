"""Tests for tools/shared_agents.py — shared agent sources materialized into plugins."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import tools.shared_agents as sa
from tools.adapters.base import parse_frontmatter

SOURCE = """---
plugins: [alpha, beta]
description: Does a thing.
model: inherit
---

You do a thing.
"""


def _run(*args: str) -> int:
    old = sys.argv
    sys.argv = ["shared_agents.py", *args]
    try:
        return sa.main()
    finally:
        sys.argv = old


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for plugin in ("alpha", "beta", "gamma"):
        (tmp_path / "plugins" / plugin / ".claude-plugin").mkdir(parents=True)
        (tmp_path / "plugins" / plugin / ".claude-plugin" / "plugin.json").write_text("{}")
    (tmp_path / "shared" / "agents").mkdir(parents=True)
    (tmp_path / "shared" / "agents" / "helper.md").write_text(SOURCE)
    monkeypatch.setattr(sa, "WORKTREE", tmp_path)
    monkeypatch.setattr(sa, "PLUGINS_DIR", tmp_path / "plugins")
    monkeypatch.setattr(sa, "SHARED_DIR", tmp_path / "shared" / "agents")
    return tmp_path


def test_materializes_one_copy_per_plugin(repo: Path) -> None:
    assert _run() == 0
    for plugin in ("alpha", "beta"):
        fm, body = parse_frontmatter(
            (repo / "plugins" / plugin / "agents" / "helper.md").read_text()
        )
        assert fm["name"] == f"{plugin}-helper"
        assert fm["description"] == "Does a thing."
        assert "plugins" not in fm
        assert body == "You do a thing.\n"
    assert not (repo / "plugins" / "gamma" / "agents").exists()
    assert _run("--check") == 0


def test_check_fails_on_hand_edited_copy(repo: Path) -> None:
    _run()
    copy = repo / "plugins" / "alpha" / "agents" / "helper.md"
    copy.write_text(copy.read_text() + "drift\n")
    assert _run("--check") == 1
    assert _run() == 0
    assert "drift" not in copy.read_text()


def test_block_list_plugins_key_is_stripped(repo: Path) -> None:
    (repo / "shared" / "agents" / "helper.md").write_text(
        SOURCE.replace("plugins: [alpha, beta]", "plugins:\n  - alpha\n  - beta")
    )
    _run()
    fm, _ = parse_frontmatter((repo / "plugins" / "beta" / "agents" / "helper.md").read_text())
    assert fm["name"] == "beta-helper"
    assert "plugins" not in fm


def test_removes_copy_when_plugin_dropped(repo: Path) -> None:
    _run()
    (repo / "shared" / "agents" / "helper.md").write_text(SOURCE.replace("alpha, beta", "alpha"))
    assert _run("--check") == 1
    assert _run() == 0
    assert not (repo / "plugins" / "beta" / "agents" / "helper.md").exists()
    assert (repo / "plugins" / "alpha" / "agents" / "helper.md").exists()


def test_refuses_to_overwrite_hand_written_agent(repo: Path) -> None:
    hand = repo / "plugins" / "alpha" / "agents" / "helper.md"
    hand.parent.mkdir(parents=True)
    hand.write_text("---\nname: alpha-helper\n---\n\nmine\n")
    assert _run() == 1
    assert hand.read_text().endswith("mine\n")


def test_rejects_unknown_plugin(repo: Path) -> None:
    (repo / "shared" / "agents" / "helper.md").write_text(SOURCE.replace("beta", "nope"))
    assert _run() == 1


def test_repo_copies_in_sync() -> None:
    """The committed tree must match its shared sources."""
    assert _run("--check") == 0
