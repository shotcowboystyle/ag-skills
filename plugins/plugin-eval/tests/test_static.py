from pathlib import Path

import pytest

from plugin_eval.layers.static import _TRIGGER_PATTERN, StaticAnalyzer
from plugin_eval.models import LayerResult


def _make_skill(tmp_path: Path, description: str, name: str = "test-skill") -> Path:
    skill_dir = tmp_path / name
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: \"{description}\"\n---\n\n"
        "# Skill\n\n## Overview\n\nBody.\n"
    )
    return skill_dir


class TestStaticAnalyzer:
    def test_analyze_valid_skill(self, sample_skill_dir: Path):
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(sample_skill_dir)
        assert isinstance(result, LayerResult)
        assert result.layer == "static"
        assert result.score > 0.5
        assert len(result.anti_patterns) == 0

    def test_analyze_poor_skill(self, poor_skill_dir: Path):
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(poor_skill_dir)
        assert result.score < 0.7
        flags = [ap.flag for ap in result.anti_patterns]
        assert "OVER_CONSTRAINED" in flags
        assert "MISSING_TRIGGER" in flags

    def test_analyze_plugin(self, sample_plugin_dir: Path):
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_plugin(sample_plugin_dir)
        assert result.layer == "static"
        assert result.score > 0.5
        assert "skill_scores" in result.sub_scores
        assert "agent_scores" in result.sub_scores

    def test_anti_pattern_penalty(self):
        analyzer = StaticAnalyzer()
        assert analyzer._anti_pattern_penalty(0) == 1.0
        assert analyzer._anti_pattern_penalty(2) == pytest.approx(0.9)
        assert analyzer._anti_pattern_penalty(10) == 0.5
        assert analyzer._anti_pattern_penalty(20) == 0.5

    def test_description_pushiness_score(self):
        analyzer = StaticAnalyzer()
        good = "Test skill for evaluation. Use when testing plugin-eval. Use PROACTIVELY for quality checks."
        weak = "A skill."
        assert analyzer._description_pushiness(good) > analyzer._description_pushiness(weak)

    def test_nested_cross_reference_resolves_from_skill_directory(self, tmp_path: Path):
        skill_dir = _make_skill(tmp_path, "Use when testing nested references.", "parent")
        nested_skill = skill_dir / "sub-skills" / "child"
        nested_skill.mkdir(parents=True)
        (nested_skill / "SKILL.md").write_text("# Child\n")
        (skill_dir / "SKILL.md").write_text(
            (skill_dir / "SKILL.md").read_text()
            + "\nSee `sub-skills/child/SKILL.md`.\n"
        )

        result = StaticAnalyzer().analyze_skill(skill_dir)

        assert "DEAD_CROSS_REF" not in [ap.flag for ap in result.anti_patterns]


def _make_skill_with_code_blocks(tmp_path: Path, blocks: int, name: str) -> Path:
    skill_dir = tmp_path / name
    skill_dir.mkdir()
    body = "\n\n".join(["```python\nprint('x')\n```"] * blocks)
    (skill_dir / "SKILL.md").write_text(
        f'---\nname: {name}\ndescription: "Use when checking code block thresholds."\n---\n\n'
        "# Skill\n\n## Usage\n\nRun it.\n\n" + body + "\n\n## Output format\n\nReturns JSON.\n"
    )
    return skill_dir


class TestCodeBlockThresholds:
    """The rubric states these thresholds in code blocks, not fence delimiters."""

    def test_two_blocks_earn_the_orchestration_bonus_that_one_does_not(self, tmp_path: Path):
        analyzer = StaticAnalyzer()
        one = analyzer.analyze_skill(_make_skill_with_code_blocks(tmp_path, 1, "one-block"))
        two = analyzer.analyze_skill(_make_skill_with_code_blocks(tmp_path, 2, "two-blocks"))
        one_score = one.sub_scores["orchestration_wiring"]
        two_score = two.sub_scores["orchestration_wiring"]
        assert two_score - one_score == pytest.approx(0.05)

    def test_five_blocks_reach_a_tier_three_blocks_do_not(self, tmp_path: Path):
        analyzer = StaticAnalyzer()
        three = analyzer.analyze_skill(_make_skill_with_code_blocks(tmp_path, 3, "three-blocks"))
        five = analyzer.analyze_skill(_make_skill_with_code_blocks(tmp_path, 5, "five-blocks"))
        three_score = three.sub_scores["structural_completeness"]
        five_score = five.sub_scores["structural_completeness"]
        assert five_score - three_score == pytest.approx(0.05)


class TestTriggerPattern:
    """Regression coverage for the broadened trigger-phrase matcher.

    plugin-dev's canonical recommendation is third-person ("This skill should be
    used when …"), and several real-world plugins use prepositional triggers
    ("Use after …", "Use before …"). The pre-2026 regex only matched the
    imperative "Use when …" form, which produced false-positive MISSING_TRIGGER
    flags against Anthropic's own examples.
    """

    @pytest.mark.parametrize(
        "description",
        [
            "Use when testing plugin-eval.",
            "Use this skill when scaffolding plugins.",
            "This skill should be used when the user asks to 'create a hook'.",
            "Used when several attempts have failed in a row.",
            "Use after editing the source-of-truth files, before committing.",
            "Use before declaring a task complete after a hard debugging session.",
            "Use immediately before a commit, push, or edit-after-failure.",
            "Use whenever you are asked to plan inside a Paperclip company.",
            "Auto-loads when working on test files.",
            "Trigger when a Bash command fails three times in a row.",
            "Use PROACTIVELY before merging.",
        ],
    )
    def test_pattern_matches_canonical_forms(self, description: str) -> None:
        assert _TRIGGER_PATTERN.search(description), (
            f"Expected trigger phrase to match in: {description!r}"
        )

    @pytest.mark.parametrize(
        "description",
        [
            "A skill.",
            "Provides hook guidance.",
            "Returns the current timestamp.",
            "Performs static analysis on plugin directories.",
        ],
    )
    def test_pattern_rejects_descriptions_without_trigger(self, description: str) -> None:
        assert not _TRIGGER_PATTERN.search(description), (
            f"Did not expect trigger match in: {description!r}"
        )

    def test_third_person_skill_does_not_flag_missing_trigger(self, tmp_path: Path) -> None:
        """Anthropic plugin-dev's canonical phrasing must not be flagged."""
        skill_dir = _make_skill(
            tmp_path,
            "This skill should be used when the user asks to 'create a hook', "
            "'add a PreToolUse hook', or 'validate tool use'.",
        )
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(skill_dir)
        flags = [ap.flag for ap in result.anti_patterns]
        assert "MISSING_TRIGGER" not in flags

    def test_prepositional_trigger_does_not_flag_missing_trigger(self, tmp_path: Path) -> None:
        skill_dir = _make_skill(
            tmp_path,
            "Self-check before a single risky action. Use immediately before a "
            "commit, push, edit-after-failure, or skip-a-verification step.",
        )
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(skill_dir)
        flags = [ap.flag for ap in result.anti_patterns]
        assert "MISSING_TRIGGER" not in flags


def _make_skill_with_frontmatter(
    tmp_path: Path, frontmatter_lines: list[str], name: str = "test-skill"
) -> Path:
    skill_dir = tmp_path / name
    skill_dir.mkdir()
    frontmatter = "\n".join(frontmatter_lines)
    (skill_dir / "SKILL.md").write_text(
        f"---\n{frontmatter}\n---\n\n# Skill\n\n## Overview\n\nBody.\n"
    )
    return skill_dir


class TestTriggerExemptions:
    """`disable-model-invocation: true` and `paths:` frontmatter should exempt
    a skill from the MISSING_TRIGGER check, because those skills are not
    auto-invoked from the description.
    """

    def test_disable_model_invocation_exempts_skill(self, tmp_path: Path) -> None:
        skill_dir = _make_skill_with_frontmatter(
            tmp_path,
            [
                "name: setup",
                "description: One-time setup that adds .claude/state/ to the project's .gitignore.",
                "disable-model-invocation: true",
            ],
        )
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(skill_dir)
        flags = [ap.flag for ap in result.anti_patterns]
        assert "MISSING_TRIGGER" not in flags, (
            "Slash-only skills should not be flagged for missing description trigger"
        )

    def test_paths_auto_load_exempts_skill(self, tmp_path: Path) -> None:
        skill_dir = _make_skill_with_frontmatter(
            tmp_path,
            [
                "name: self-evaluate",
                "description: Self-critical evaluation guard for test/spec files.",
                'paths: "**/*test*,**/*spec*"',
            ],
        )
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(skill_dir)
        flags = [ap.flag for ap in result.anti_patterns]
        assert "MISSING_TRIGGER" not in flags, (
            "Path-triggered skills should not be flagged for missing description trigger"
        )

    def test_disable_model_invocation_false_still_checks_trigger(
        self, tmp_path: Path
    ) -> None:
        skill_dir = _make_skill_with_frontmatter(
            tmp_path,
            [
                "name: model-invocable",
                "description: A description without a trigger phrase whatsoever.",
                "disable-model-invocation: false",
            ],
        )
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(skill_dir)
        flags = [ap.flag for ap in result.anti_patterns]
        assert "MISSING_TRIGGER" in flags, (
            "Model-invocable skills without a trigger phrase must still be flagged"
        )

    def test_empty_paths_value_still_checks_trigger(self, tmp_path: Path) -> None:
        skill_dir = _make_skill_with_frontmatter(
            tmp_path,
            [
                "name: bad-paths",
                "description: Some skill description that lacks the trigger phrase.",
                'paths: ""',
            ],
        )
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(skill_dir)
        flags = [ap.flag for ap in result.anti_patterns]
        assert "MISSING_TRIGGER" in flags


_GOOD_AGENT = """---
name: p-api-reviewer
description: Review an API diff for breaking changes. Use when a PR touches route handlers.
model: sonnet
tools: Read, Grep, Glob
---

Review the API changes in the given diff.

## Procedure

1. List changed route handlers.
2. Compare old and new shapes.
3. Mark each change breaking or not.

## Output

A table of `endpoint | change | breaking?`, then a verdict line.
"""


def _write_agent(tmp_path: Path, text: str, stem: str = "api-reviewer") -> Path:
    path = tmp_path / "p" / "agents" / f"{stem}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


class TestAnalyzeAgent:
    def test_well_shaped_agent_scores_full(self, tmp_path: Path) -> None:
        result = StaticAnalyzer().analyze_agent(_write_agent(tmp_path, _GOOD_AGENT))
        assert result.sub_scores == {
            "frontmatter_quality": 1.0,
            "tool_scoping": 1.0,
            "model_tier": 1.0,
            "procedure": 1.0,
            "output_contract": 1.0,
            "uniqueness": 1.0,
        }
        assert result.score == 1.0

    def test_capability_list_persona_scores_low(self, tmp_path: Path) -> None:
        text = (
            "---\nname: x\ndescription: Expert.\nmodel: opus\n---\n\n"
            "You are an expert.\n\n## Capabilities\n- REST\n- gRPC\n"
        )
        sub = StaticAnalyzer().analyze_agent(_write_agent(tmp_path, text, "x")).sub_scores
        assert sub["frontmatter_quality"] == 0.5  # name and model, no trigger, too short
        assert sub["tool_scoping"] == 0.0
        assert sub["model_tier"] == 0.5  # opus with no justification line
        assert sub["procedure"] == 0.0
        assert sub["output_contract"] == 0.0

    def test_read_only_role_with_write_tools(self, tmp_path: Path) -> None:
        text = _GOOD_AGENT.replace("tools: Read, Grep, Glob", "tools: Read, Edit")
        sub = StaticAnalyzer().analyze_agent(_write_agent(tmp_path, text)).sub_scores
        assert sub["tool_scoping"] == 0.5

    def test_justified_opus_and_numbered_headings(self, tmp_path: Path) -> None:
        text = _GOOD_AGENT.replace("model: sonnet", "model: opus").replace(
            "Review the API changes", "Model: opus, because it traces contracts.\n\nReview the API changes"
        )
        text = text.replace("1. List", "### 1. List").replace("2. Compare", "### 2: Compare")
        sub = StaticAnalyzer().analyze_agent(_write_agent(tmp_path, text)).sub_scores
        assert sub["model_tier"] == 1.0
        assert sub["procedure"] == 1.0

    def test_steps_inside_code_fences_do_not_count(self, tmp_path: Path) -> None:
        text = _GOOD_AGENT.replace("1. List", "```\n1. List").replace(
            "3. Mark each change breaking or not.", "3. Mark each change breaking or not.\n```"
        )
        sub = StaticAnalyzer().analyze_agent(_write_agent(tmp_path, text)).sub_scores
        assert sub["procedure"] == 0.0

    def test_duplicates_zero_uniqueness(self, tmp_path: Path) -> None:
        result = StaticAnalyzer().analyze_agent(_write_agent(tmp_path, _GOOD_AGENT), duplicates=2)
        assert result.sub_scores["uniqueness"] == 0.0
