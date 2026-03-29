from pathlib import Path

from code_agent.skills.skill_manager import SkillManager
from code_agent.tools.activate_skill import ActivateSkillTool


def _create_manager_with_skill(tmp_path: Path) -> SkillManager:
    skills_dir = tmp_path / ".code-agent" / "skills" / "test-skill"
    skills_dir.mkdir(parents=True)
    (skills_dir / "SKILL.md").write_text(
        "---\nname: test-skill\ndescription: A test skill\n---\n\n# Instructions\nDo the thing"
    )
    manager = SkillManager(workspace_dir=tmp_path)
    manager.discover_skills()
    return manager


class TestActivateSkillTool:
    def test_get_name(self, tmp_path: Path) -> None:
        manager = _create_manager_with_skill(tmp_path)
        tool = ActivateSkillTool(skill_manager=manager)
        assert tool.get_name() == "activate_skill"

    def test_declaration_includes_skill_names(self, tmp_path: Path) -> None:
        manager = _create_manager_with_skill(tmp_path)
        tool = ActivateSkillTool(skill_manager=manager)
        decl = tool.get_declaration()
        assert "test-skill" in decl.parameters["properties"]["skill_name"]["enum"]

    def test_needs_confirmation_false(self, tmp_path: Path) -> None:
        manager = _create_manager_with_skill(tmp_path)
        tool = ActivateSkillTool(skill_manager=manager)
        assert tool.needs_confirmation() is False

    def test_execute_valid_skill(self, tmp_path: Path) -> None:
        manager = _create_manager_with_skill(tmp_path)
        tool = ActivateSkillTool(skill_manager=manager)
        result = tool.execute(skill_name="test-skill")
        assert result.error is None
        assert "# Instructions" in result.content
        assert "Do the thing" in result.content
        assert manager.is_skill_active("test-skill")

    def test_execute_unknown_skill(self, tmp_path: Path) -> None:
        manager = _create_manager_with_skill(tmp_path)
        tool = ActivateSkillTool(skill_manager=manager)
        result = tool.execute(skill_name="nonexistent")
        assert result.error is not None
        assert "not found" in result.error
        assert "test-skill" in result.error
