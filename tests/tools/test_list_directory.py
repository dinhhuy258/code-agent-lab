from code_agent.tools.list_directory import ListDirectoryTool


class TestListDirectoryTool:
    def test_get_name(self) -> None:
        assert ListDirectoryTool().get_name() == "list_directory"

    def test_get_declaration(self) -> None:
        decl = ListDirectoryTool().get_declaration()
        assert decl.name == "list_directory"
        assert "dir_path" in decl.parameters["properties"]

    def test_needs_confirmation(self) -> None:
        assert ListDirectoryTool().needs_confirmation() is False

    def test_list_directory(self, tmp_path) -> None:
        (tmp_path / "a.py").write_text("x")
        (tmp_path / "b.txt").write_text("y")
        (tmp_path / "subdir").mkdir()
        tool = ListDirectoryTool()
        result = tool.execute(dir_path=str(tmp_path))
        assert result.error is None
        assert "a.py" in result.content
        assert "b.txt" in result.content
        assert "subdir" in result.content

    def test_not_a_directory(self, tmp_path) -> None:
        f = tmp_path / "file.txt"
        f.write_text("x")
        tool = ListDirectoryTool()
        result = tool.execute(dir_path=str(f))
        assert result.error is not None

    def test_nonexistent_directory(self) -> None:
        tool = ListDirectoryTool()
        result = tool.execute(dir_path="/nonexistent/path")
        assert result.error is not None
