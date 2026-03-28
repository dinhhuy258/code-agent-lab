from code_agent.tools.write_file import WriteFileTool

class TestWriteFileTool:
    def test_get_name(self) -> None:
        assert WriteFileTool().get_name() == "write_file"

    def test_needs_confirmation(self) -> None:
        assert WriteFileTool().needs_confirmation() is True

    def test_write_new_file(self, tmp_path) -> None:
        file_path = str(tmp_path / "new.txt")
        tool = WriteFileTool()
        result = tool.execute(file_path=file_path, content="hello world")
        assert result.error is None
        assert (tmp_path / "new.txt").read_text() == "hello world"

    def test_write_creates_parent_dirs(self, tmp_path) -> None:
        file_path = str(tmp_path / "sub" / "deep" / "new.txt")
        tool = WriteFileTool()
        result = tool.execute(file_path=file_path, content="nested")
        assert result.error is None
        assert "nested" in (tmp_path / "sub" / "deep" / "new.txt").read_text()

    def test_overwrite_existing_file(self, tmp_path) -> None:
        f = tmp_path / "existing.txt"
        f.write_text("old content")
        tool = WriteFileTool()
        result = tool.execute(file_path=str(f), content="new content")
        assert result.error is None
        assert f.read_text() == "new content"

    def test_empty_file_path(self) -> None:
        tool = WriteFileTool()
        result = tool.execute(file_path="", content="hello")
        assert result.error is not None
