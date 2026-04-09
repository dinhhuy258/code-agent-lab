"""Tests for the public prompt API."""

from pathlib import Path

from code_agent.prompts import get_system_instruction
from code_agent.skills.skill_manager import SkillManager


def _make_skill_manager() -> SkillManager:
    return SkillManager(workspace_dir=Path.cwd())


class TestGetSystemInstruction:
    def test_returns_non_empty_string(self) -> None:
        result = get_system_instruction(skill_manager=_make_skill_manager())
        assert isinstance(result, str)
        assert len(result) > 0

    def test_includes_preamble(self) -> None:
        result = get_system_instruction(skill_manager=_make_skill_manager())
        assert "Code Agent" in result
