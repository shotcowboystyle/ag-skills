#!/usr/bin/env python3
"""Materialize shared agents into the plugins that list them.

A shared agent lives at `shared/agents/<stem>.md`. Its frontmatter has no `name:`;
instead a `plugins:` list names the plugins that ship it. For each listed plugin this
writes `plugins/<plugin>/agents/<stem>.md` with `name: <plugin>-<stem>` and the
`plugins:` key removed, so Claude Code (which reads `plugins/` directly) and every
adapter see an ordinary per-plugin agent.

Usage:
    python tools/shared_agents.py          # write copies, delete stale ones
    python tools/shared_agents.py --check  # exit 1 if any copy is missing or drifted
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.adapters.base import PLUGINS_DIR, WORKTREE, parse_frontmatter, read_file

SHARED_DIR = WORKTREE / "shared" / "agents"
MARKER = "# Generated from shared/agents/"


def render(source: Path, plugin: str) -> str:
    """Return the materialized agent file for one plugin."""
    text = read_file(source)
    end = text.find("\n---", 3)
    lines = text[4:end].split("\n")
    kept: list[str] = []
    skipping = False
    for line in lines:
        if re.match(r"^plugins:", line):
            skipping = True
            continue
        if skipping and line.startswith((" ", "\t")):
            continue
        skipping = False
        kept.append(line)
    header = [
        f"{MARKER}{source.name} by `make generate-all`. Edit that file, not this one.",
        f"name: {plugin}-{source.stem}",
    ]
    return "---\n" + "\n".join(header + kept) + text[end:]


def build() -> dict[Path, str]:
    """Map every materialized path to its expected content."""
    out: dict[Path, str] = {}
    for source in sorted(SHARED_DIR.glob("*.md")) if SHARED_DIR.is_dir() else []:
        fm, _ = parse_frontmatter(read_file(source))
        plugins = fm.get("plugins")
        if not isinstance(plugins, list) or not plugins:
            raise ValueError(f"{source}: `plugins:` must list at least one plugin")
        if "name" in fm:
            raise ValueError(f"{source}: drop `name:`; it is set per plugin")
        for plugin in plugins:
            if not (PLUGINS_DIR / plugin / ".claude-plugin" / "plugin.json").is_file():
                raise ValueError(f"{source}: unknown plugin {plugin!r}")
            out[PLUGINS_DIR / plugin / "agents" / source.name] = render(source, plugin)
    return out


def is_materialized(path: Path) -> bool:
    return path.is_file() and MARKER in read_file(path).split("\n---", 1)[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="Report drift; write nothing.")
    args = parser.parse_args()

    try:
        expected = build()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    problems: list[str] = []
    for path, content in expected.items():
        rel = path.relative_to(WORKTREE)
        if path.exists() and not is_materialized(path):
            # Never overwrite a hand-written per-plugin agent.
            problems.append(f"{rel}: hand-written agent in the way; delete it first")
        elif not path.exists() or read_file(path) != content:
            if args.check:
                problems.append(f"{rel}: out of sync with shared/agents/{path.name}")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
                print(f"  + {rel}")

    for path in sorted(PLUGINS_DIR.glob("*/agents/*.md")):
        if path not in expected and is_materialized(path):
            rel = path.relative_to(WORKTREE)
            if args.check:
                problems.append(f"{rel}: stale copy; its shared source no longer lists it")
            else:
                path.unlink()
                print(f"  - {rel}")

    for p in problems:
        print(f"Error: {p}", file=sys.stderr)
    if problems and args.check:
        print("Run `make generate-all` and commit the result.", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
