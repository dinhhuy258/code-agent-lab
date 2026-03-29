from pathlib import Path

from code_agent.skills.skill_manager import SkillManager


class TestSkillManager:
    def test_discover_no_skills_dir(self, tmp_path: Path) -> None:
        manager = SkillManager(workspace_dir=tmp_path)
        manager.discover_skills()
        assert manager.get_skills() == []

    def test_discover_with_skills(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / ".code-agent" / "skills"
        skill_a = skills_dir / "skill-a"
        skill_a.mkdir(parents=True)
        (skill_a / "SKILL.md").write_text(
            "---\nname: skill-a\ndescription: Desc A\n---\nBody A"
        )

        manager = SkillManager(workspace_dir=tmp_path)
        manager.discover_skills()
        skills = manager.get_skills()
        assert len(skills) == 1
        assert skills[0].name == "skill-a"

    def test_get_skill_found(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / ".code-agent" / "skills" / "my-skill"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: Test\n---\nBody"
        )

        manager = SkillManager(workspace_dir=tmp_path)
        manager.discover_skills()
        assert manager.get_skill("my-skill") is not None

    def test_get_skill_not_found(self, tmp_path: Path) -> None:
        manager = SkillManager(workspace_dir=tmp_path)
        manager.discover_skills()
        assert manager.get_skill("nonexistent") is None

    def test_activate_skill(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / ".code-agent" / "skills" / "my-skill"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: Test\n---\nBody"
        )

        manager = SkillManager(workspace_dir=tmp_path)
        manager.discover_skills()

        assert not manager.is_skill_active("my-skill")
        skill = manager.activate_skill("my-skill")
        assert skill is not None
        assert skill.name == "my-skill"
        assert manager.is_skill_active("my-skill")

    def test_activate_unknown_skill(self, tmp_path: Path) -> None:
        manager = SkillManager(workspace_dir=tmp_path)
        manager.discover_skills()
        assert manager.activate_skill("nonexistent") is None

    def test_duplicate_skill_last_wins(self, tmp_path: Path) -> None:
        skills_dir = tmp_path / ".code-agent" / "skills"
        # Top-level SKILL.md with name "dupe"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text(
            "---\nname: dupe\ndescription: First\n---\nFirst body"
        )
        # Subdirectory SKILL.md with same name
        sub = skills_dir / "dupe"
        sub.mkdir()
        (sub / "SKILL.md").write_text(
            "---\nname: dupe\ndescription: Second\n---\nSecond body"
        )

        manager = SkillManager(workspace_dir=tmp_path)
        manager.discover_skills()
        skill = manager.get_skill("dupe")
        assert skill is not None
        assert skill.description == "Second"
