from code_agent.tools.grep_search import GrepSearchTool

class TestGrepSearchTool:
    def test_get_name(self) -> None:
        assert GrepSearchTool().get_name() == "grep_search"

    def test_get_declaration(self) -> None:
        decl = GrepSearchTool().get_declaration()
        assert decl.name == "grep_search"
        assert "pattern" in decl.parameters["properties"]

    def test_needs_confirmation(self) -> None:
        assert GrepSearchTool().needs_confirmation() is False

    def test_find_pattern(self, tmp_path) -> None:
        (tmp_path / "a.py").write_text("def hello():\n    pass\n")
        (tmp_path / "b.py").write_text("def world():\n    pass\n")
        tool = GrepSearchTool()
        result = tool.execute(pattern="hello", dir_path=str(tmp_path))
        assert result.error is None
        assert "hello" in result.content
        assert "a.py" in result.content

    def test_no_matches(self, tmp_path) -> None:
        (tmp_path / "a.py").write_text("def hello():\n    pass\n")
        tool = GrepSearchTool()
        result = tool.execute(pattern="nonexistent_xyz", dir_path=str(tmp_path))
        assert result.error is None
        assert "No matches" in result.content

    def test_case_insensitive(self, tmp_path) -> None:
        (tmp_path / "a.py").write_text("Hello World\n")
        tool = GrepSearchTool()
        result = tool.execute(pattern="hello", dir_path=str(tmp_path), case_sensitive=False)
        assert "Hello" in result.content

    def test_include_pattern(self, tmp_path) -> None:
        (tmp_path / "a.py").write_text("target\n")
        (tmp_path / "b.txt").write_text("target\n")
        tool = GrepSearchTool()
        result = tool.execute(pattern="target", dir_path=str(tmp_path), include_pattern="*.py")
        assert "a.py" in result.content
        assert "b.txt" not in result.content
