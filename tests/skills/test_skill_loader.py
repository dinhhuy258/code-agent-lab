from pathlib import Path

from code_agent.skills.skill_loader import (
    load_skill_from_file,
    load_skills_from_dir,
    parse_frontmatter,
)


class TestParseFrontmatter:
    def test_valid_frontmatter(self) -> None:
        content = "---\nname: my-skill\ndescription: A test skill\n---\n\n# Body\nHello"
        meta, body = parse_frontmatter(content)
        assert meta["name"] == "my-skill"
        assert meta["description"] == "A test skill"
        assert body.strip() == "# Body\nHello"

    def test_missing_frontmatter(self) -> None:
        content = "# Just a body\nNo frontmatter here"
        meta, body = parse_frontmatter(content)
        assert meta == {}
        assert body == content

    def test_description_with_colon(self) -> None:
        content = '---\nname: my-skill\ndescription: "Has: a colon"\n---\nBody'
        meta, body = parse_frontmatter(content)
        assert meta["description"] == "Has: a colon"

    def test_empty_content(self) -> None:
        meta, body = parse_frontmatter("")
        assert meta == {}
        assert body == ""


class TestLoadSkillFromFile:
    def test_valid_skill_file(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            "---\nname: my-skill\ndescription: A skill\n---\n\nInstructions here"
        )

        skill = load_skill_from_file(skill_file)
        assert skill is not None
        assert skill.name == "my-skill"
        assert skill.description == "A skill"
        assert "Instructions here" in skill.body
        assert skill.location == str(skill_file)

    def test_name_fallback_to_directory(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / "code-reviewer"
        skill_dir.mkdir()
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text("---\ndescription: Reviews code\n---\nBody")

        skill = load_skill_from_file(skill_file)
        assert skill is not None
        assert skill.name == "code-reviewer"

    def test_missing_description(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text("---\nname: my-skill\n---\nBody")

        skill = load_skill_from_file(skill_file)
        assert skill is not None
        assert skill.description == ""

    def test_no_frontmatter(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / "raw-skill"
        skill_dir.mkdir()
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text("# Just instructions\nDo stuff")

        skill = load_skill_from_file(skill_file)
        assert skill is not None
        assert skill.name == "raw-skill"
        assert skill.description == ""
        assert "Just instructions" in skill.body


class TestLoadSkillsFromDir:
    def test_loads_multiple_skills(self, tmp_path: Path) -> None:
        for name in ["skill-a", "skill-b"]:
            d = tmp_path / name
            d.mkdir()
            (d / "SKILL.md").write_text(
                f"---\nname: {name}\ndescription: Desc {name}\n---\nBody {name}"
            )

        skills = load_skills_from_dir(tmp_path)
        names = {s.name for s in skills}
        assert names == {"skill-a", "skill-b"}

    def test_top_level_skill_md(self, tmp_path: Path) -> None:
        (tmp_path / "SKILL.md").write_text(
            "---\nname: top-skill\ndescription: Top\n---\nBody"
        )
        skills = load_skills_from_dir(tmp_path)
        assert len(skills) == 1
        assert skills[0].name == "top-skill"

    def test_nonexistent_directory(self) -> None:
        skills = load_skills_from_dir(Path("/nonexistent/path"))
        assert skills == []

    def test_malformed_file_skipped(self, tmp_path: Path) -> None:
        good = tmp_path / "good"
        good.mkdir()
        (good / "SKILL.md").write_text(
            "---\nname: good-skill\ndescription: Good\n---\nBody"
        )

        bad = tmp_path / "bad"
        bad.mkdir()
        bad_file = bad / "SKILL.md"
        bad_file.write_text("")  # empty but valid — should still load

        skills = load_skills_from_dir(tmp_path)
        assert len(skills) == 2
