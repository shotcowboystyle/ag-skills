from pathlib import Path

from plugin_eval.snapshot import (
    SnapshotEntry,
    agent_duplicate_counts,
    build_snapshot,
    compare_snapshot,
    skill_digest,
)


def make_skill(root: Path, body: str, name: str = "s") -> Path:
    d = root / "p" / "skills" / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Use when x.\n---\n{body}\n")
    return d


def test_digest_changes_with_content(tmp_path: Path) -> None:
    d = make_skill(tmp_path, "one")
    first = skill_digest(d)
    (d / "SKILL.md").write_text((d / "SKILL.md").read_text() + "two\n")
    assert skill_digest(d) != first


def test_digest_covers_references(tmp_path: Path) -> None:
    d = make_skill(tmp_path, "one")
    first = skill_digest(d)
    (d / "references").mkdir()
    (d / "references" / "x.md").write_text("detail")
    assert skill_digest(d) != first


def test_digest_tracks_whether_cross_reference_targets_exist(tmp_path: Path) -> None:
    # The static layer flags a cross-reference whose target is missing, so creating
    # the target can change the score of a skill whose own files did not change.
    a = make_skill(tmp_path, "See skills/b and skills/c/extra for the details.", name="a")
    missing = skill_digest(a)
    b = make_skill(tmp_path, "No references here.", name="b")
    after_b = skill_digest(a)
    assert after_b != missing
    c = make_skill(tmp_path, "one", name="c")
    assert skill_digest(a) == after_b  # c exists, but the nested c/extra does not
    (c / "extra").mkdir()
    assert skill_digest(a) != after_b
    b_before = skill_digest(b)
    make_skill(tmp_path, "one", name="d")
    assert skill_digest(b) == b_before


def test_digest_uses_the_sub_skills_fallback(tmp_path: Path) -> None:
    d = make_skill(tmp_path, "See sub-skills/part.", name="a")
    before = skill_digest(d)
    (d / "sub-skills" / "part").mkdir(parents=True)
    assert skill_digest(d) != before


def test_digest_does_not_depend_on_the_parser(tmp_path: Path, monkeypatch) -> None:
    # A change to the parser's pattern must move scores, not digests, so the
    # snapshot test fails instead of marking the skill stale.
    import re

    from plugin_eval import parser

    d = make_skill(tmp_path, "See skills/b for the details.", name="a")
    before = skill_digest(d)
    monkeypatch.setattr(parser, "_CROSS_REFERENCE_PATTERN", re.compile(r"(references/[a-z-]+)"))
    assert skill_digest(d) == before


def test_digest_ignores_line_endings(tmp_path: Path) -> None:
    d = make_skill(tmp_path, "one\ntwo")
    lf = skill_digest(d)
    md = d / "SKILL.md"
    md.write_bytes(md.read_bytes().replace(b"\n", b"\r\n"))
    assert skill_digest(d) == lf


def entry(digest: str, score: float) -> SnapshotEntry:
    return SnapshotEntry(
        digest=digest,
        static_score=score,
        sub_scores={"a": score},
        composite=score * 100,
        badge="Gold",
    )


def test_compare_skips_changed_content_and_flags_score_drift() -> None:
    saved = {"p/one": entry("d1", 0.8), "p/two": entry("d2", 0.8)}
    current = {"p/one": entry("d1", 0.7), "p/two": entry("CHANGED", 0.1)}
    result = compare_snapshot(saved, current)
    assert result.matched == 1
    assert result.stale == 1
    assert len(result.diffs) == 1
    assert "p/one" in result.diffs[0]


def _agent(root: Path, plugin: str, body: str, frontmatter: str = "") -> Path:
    path = root / plugin / "agents" / "x.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{frontmatter}name: {plugin}-x\ntools: Read\n---\n{body}\n")
    return path


def test_duplicate_counts_skip_same_plugin_and_shared_copies(tmp_path: Path) -> None:
    a = _agent(tmp_path, "a", "Same body.")
    b = _agent(tmp_path, "b", "Same body.")
    shared = "# Generated from shared/agents/x.md by `make generate-all`.\n"
    c = _agent(tmp_path, "c", "Shared body.", shared)
    d = _agent(tmp_path, "d", "Shared body.", shared)
    assert agent_duplicate_counts(tmp_path) == {a: 1, b: 1, c: 0, d: 0}


def test_snapshot_includes_agents(tmp_path: Path) -> None:
    make_skill(tmp_path, "body")
    _agent(tmp_path, "p", "Body.")
    snap = build_snapshot(tmp_path)
    assert set(snap) == {"p/s", "p/agents/x"}
    assert set(snap["p/agents/x"].sub_scores) == {
        "frontmatter_quality",
        "tool_scoping",
        "model_tier",
        "procedure",
        "output_contract",
        "uniqueness",
    }
