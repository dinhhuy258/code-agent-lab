"""Tests for memory discovery (AGENT.md file loading).

"""

from pathlib import Path

from code_agent.prompts.user_context_loader import load_user_context

class TestLoadUserContext:
    def test_no_files_returns_empty(self, tmp_path: Path) -> None:
        result = load_user_context(project_dir=tmp_path)
        assert result.global_context is None
        assert result.project_context is None

    def test_loads_global_context(self, tmp_path: Path) -> None:
        global_dir = tmp_path / ".agent"
        global_dir.mkdir()
        (global_dir / "AGENT.md").write_text("Global instructions")

        result = load_user_context(
            project_dir=tmp_path / "some_project",
            global_agent_dir=global_dir,
        )
        assert result.global_context is not None
        assert "Global instructions" in result.global_context

    def test_loads_project_context(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        agent_dir = project_dir / ".agent"
        agent_dir.mkdir()
        (agent_dir / "AGENT.md").write_text("Project rules")

        result = load_user_context(project_dir=project_dir)
        assert result.project_context is not None
        assert "Project rules" in result.project_context

    def test_loads_both_global_and_project(self, tmp_path: Path) -> None:
        global_dir = tmp_path / "global_agent"
        global_dir.mkdir()
        (global_dir / "AGENT.md").write_text("Global prefs")

        project_dir = tmp_path / "project"
        project_dir.mkdir()
        agent_dir = project_dir / ".agent"
        agent_dir.mkdir()
        (agent_dir / "AGENT.md").write_text("Project rules")

        result = load_user_context(
            project_dir=project_dir,
            global_agent_dir=global_dir,
        )
        assert result.global_context is not None
        assert "Global prefs" in result.global_context
        assert result.project_context is not None
        assert "Project rules" in result.project_context

    def test_missing_agent_dir_returns_none(self, tmp_path: Path) -> None:
        result = load_user_context(
            project_dir=tmp_path,
            global_agent_dir=tmp_path / "nonexistent",
        )
        assert result.global_context is None
        assert result.project_context is None

    def test_returns_raw_content(self, tmp_path: Path) -> None:
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        agent_dir = project_dir / ".agent"
        agent_dir.mkdir()
        (agent_dir / "AGENT.md").write_text("Rules here")

        result = load_user_context(project_dir=project_dir)
        assert result.project_context == "Rules here"
