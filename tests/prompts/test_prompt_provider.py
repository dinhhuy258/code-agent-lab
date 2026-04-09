"""Tests for PromptProvider orchestrator."""

from pathlib import Path

from code_agent.prompts.prompt_provider import PromptProvider
from code_agent.skills.skill_manager import SkillManager


def _make_skill_manager() -> SkillManager:
    return SkillManager(workspace_dir=Path.cwd())


class TestPromptProvider:
    def test_returns_non_empty_prompt(self) -> None:
        provider = PromptProvider(skill_manager=_make_skill_manager())
        result = provider.get_system_instruction()
        assert len(result) > 0

    def test_includes_preamble(self) -> None:
        provider = PromptProvider(skill_manager=_make_skill_manager())
        result = provider.get_system_instruction()
        assert "Code Agent" in result

    def test_no_triple_newlines(self) -> None:
        provider = PromptProvider(skill_manager=_make_skill_manager())
        result = provider.get_system_instruction()
        assert "\n\n\n" not in result
