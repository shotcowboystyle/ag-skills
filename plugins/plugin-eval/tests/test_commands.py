"""Slash commands must defer scoring to the engine and survive a caller-relative path."""

from pathlib import Path

import pytest

COMMANDS = sorted((Path(__file__).parent.parent / "commands").glob("*.md"))


@pytest.mark.parametrize("command", COMMANDS, ids=lambda p: p.name)
def test_command_does_not_copy_weights(command: Path):
    text = command.read_text().lower()
    assert "blend weight" not in text
    assert "dimension weights" not in text


@pytest.mark.parametrize("command", COMMANDS, ids=lambda p: p.name)
def test_command_runs_cli_from_plugin_root_without_cd(command: Path):
    text = command.read_text()
    assert "cd plugins/plugin-eval" not in text
    assert 'cd "${CLAUDE_PLUGIN_ROOT}"' not in text
    assert 'uv run --directory "${CLAUDE_PLUGIN_ROOT}" plugin-eval' in text
