from code_agent.tools.read_file import ReadFileTool

class TestReadFileTool:
    def test_get_name(self) -> None:
        assert ReadFileTool().get_name() == "read_file"

    def test_get_declaration(self) -> None:
        decl = ReadFileTool().get_declaration()
        assert decl.name == "read_file"
        assert "file_path" in decl.parameters["properties"]

    def test_needs_confirmation(self) -> None:
        assert ReadFileTool().needs_confirmation() is False

    def test_read_file(self, tmp_path) -> None:
        f = tmp_path / "test.txt"
        f.write_text("hello world\nsecond line")
        tool = ReadFileTool()
        result = tool.execute(file_path=str(f))
        assert result.error is None
        assert "hello world" in result.content
        assert "second line" in result.content

    def test_read_file_with_line_range(self, tmp_path) -> None:
        f = tmp_path / "test.txt"
        f.write_text("line1\nline2\nline3\nline4\nline5")
        tool = ReadFileTool()
        result = tool.execute(file_path=str(f), start_line=2, end_line=4)
        assert "line2" in result.content
        assert "line4" in result.content
        assert "line1" not in result.content
        assert "line5" not in result.content

    def test_file_not_found(self) -> None:
        tool = ReadFileTool()
        result = tool.execute(file_path="/nonexistent/file.txt")
        assert result.error is not None

    def test_line_numbers_included(self, tmp_path) -> None:
        f = tmp_path / "test.txt"
        f.write_text("hello\nworld")
        tool = ReadFileTool()
        result = tool.execute(file_path=str(f))
        assert "1:" in result.content or "1\t" in result.content
