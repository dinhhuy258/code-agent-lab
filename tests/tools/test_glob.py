
from code_agent.tools.glob import GlobTool


class TestGlobTool:
    def test_get_name(self) -> None:
        assert GlobTool().get_name() == "glob"

    def test_get_declaration(self) -> None:
        decl = GlobTool().get_declaration()
        assert decl.name == "glob"
        assert "pattern" in decl.parameters["properties"]

    def test_needs_confirmation(self) -> None:
        assert GlobTool().needs_confirmation() is False

    def test_find_python_files(self, tmp_path) -> None:
        (tmp_path / "a.py").write_text("x")
        (tmp_path / "b.txt").write_text("y")
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "c.py").write_text("z")
        tool = GlobTool()
        result = tool.execute(pattern="**/*.py", dir_path=str(tmp_path))
        assert result.error is None
        assert "a.py" in result.content
        assert "c.py" in result.content
        assert "b.txt" not in result.content

    def test_no_matches(self, tmp_path) -> None:
        tool = GlobTool()
        result = tool.execute(pattern="*.xyz", dir_path=str(tmp_path))
        assert result.error is None
        assert "No files found" in result.content

    def test_invalid_directory(self) -> None:
        tool = GlobTool()
        result = tool.execute(pattern="*.py", dir_path="/nonexistent/path")
        assert result.error is not None
