"""Tests for the block-no-verify hook pattern and install script documented in the plugin."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[2] / "plugins" / "block-no-verify"
SKILL = PLUGIN / "skills" / "block-no-verify-hook" / "SKILL.md"
COMMAND = PLUGIN / "commands" / "block-no-verify.md"

BLOCKED = [
    "git commit --no-verify -m x",
    "git push --no-verify",
    "git commit -n -m x",
    "git commit -nm x",
    "git -C /repo commit --no-veri -m x",
    "git merge --no-gpg-sign feature",
    "git rebase --no-verify main",
    "cd x && git commit --no-verify",
    "sudo git commit --no-verify",
    "if git commit --no-verify; then :; fi",
    "/usr/bin/git commit --no-verify",
    "git commit -m x\ngit push --no-verify",
    'git commit -m "a" --no-verify',
    "git\tcommit\t--no-verify",
]

ALLOWED = [
    "npm version patch --no-git-tag-version",
    "git commit -m x && echo -n",
    "git commit -m x",
    "git commit -m x\necho -n hi",
    "git commit -m x; echo -n y",
    "git commit --amend --no-edit",
    "git push --no-verbose",
    "git push -n",
    "git log -n 5",
    "echo --no-verify",
    "mygit commit --no-verify",
]


def _code_blocks(path: Path, lang: str) -> list[str]:
    return re.findall(rf"```{lang}\n(.*?)```", path.read_text(), re.DOTALL)


def _hook_commands(path: Path) -> list[str]:
    commands = []
    for block in _code_blocks(path, "json"):
        for match in re.finditer(r'"command": ("(?:[^"\\]|\\.)*")', block):
            command = json.loads(match.group(1))
            if "BLOCKED: --no-verify" in command:
                commands.append(command)
    return commands


def _run_hook(hook: str, command: str) -> int:
    payload = json.dumps(
        {
            "tool_name": "Bash",
            "tool_input": {"command": command, "description": "never --no-verify"},
            "cwd": "/tmp/git commit -n",
        }
    )
    return subprocess.run(
        ["sh", "-c", hook], input=payload, text=True, capture_output=True, check=False
    ).returncode


HOOK = _hook_commands(SKILL)[0]
INSTALL = next(b for b in _code_blocks(SKILL, "bash") if "python3 -" in b)


def test_every_documented_copy_matches() -> None:
    copies = _hook_commands(SKILL) + _hook_commands(COMMAND)
    assert json.dumps(HOOK) in INSTALL
    assert set(copies) == {HOOK}


@pytest.mark.parametrize("command", BLOCKED)
def test_blocks_bypass_flags(command: str) -> None:
    assert _run_hook(HOOK, command) == 2


@pytest.mark.parametrize("command", ALLOWED)
def test_allows_lookalikes(command: str) -> None:
    assert _run_hook(HOOK, command) == 0


def test_install_script_merges_and_backs_up(tmp_path: Path) -> None:
    settings = tmp_path / ".claude" / "settings.json"
    settings.parent.mkdir()
    old_hook = {
        "type": "command",
        "command": "echo 'BLOCKED: --no-verify old' >&2; exit 2",
    }
    other = {"matcher": "Edit", "hooks": [{"type": "command", "command": "true"}]}
    original = {
        "model": "opus",
        "hooks": {"PreToolUse": [other, {"matcher": "Bash", "hooks": [old_hook]}]},
    }
    settings.write_text(json.dumps(original))

    subprocess.run(["bash", "-c", INSTALL], cwd=tmp_path, check=True)
    (backup,) = settings.parent.glob("settings.json.bak.*")
    assert json.loads(backup.read_text()) == original

    subprocess.run(["bash", "-c", INSTALL], cwd=tmp_path, check=True)
    merged = json.loads(settings.read_text())
    assert merged["model"] == "opus"
    assert merged["hooks"]["PreToolUse"] == [
        other,
        {"matcher": "Bash", "hooks": [{"type": "command", "command": HOOK}]},
    ]
