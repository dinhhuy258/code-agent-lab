from code_agent.tools.replace import ReplaceTool


class TestReplaceTool:
    def test_get_name(self) -> None:
        assert ReplaceTool().get_name() == "replace"

    def test_needs_confirmation(self) -> None:
        assert ReplaceTool().needs_confirmation() is True

    def test_single_replacement(self, tmp_path) -> None:
        f = tmp_path / "test.py"
        f.write_text("def hello():\n    return 'hello'\n")
        tool = ReplaceTool()
        result = tool.execute(
            file_path=str(f),
            old_string="return 'hello'",
            new_string="return 'world'",
        )
        assert result.error is None
        assert "return 'world'" in f.read_text()

    def test_no_match_found(self, tmp_path) -> None:
        f = tmp_path / "test.py"
        f.write_text("def hello():\n    pass\n")
        tool = ReplaceTool()
        result = tool.execute(
            file_path=str(f),
            old_string="nonexistent text",
            new_string="replacement",
        )
        assert result.error is not None

    def test_multiple_matches_without_allow_multiple(self, tmp_path) -> None:
        f = tmp_path / "test.py"
        f.write_text("foo\nfoo\n")
        tool = ReplaceTool()
        result = tool.execute(
            file_path=str(f),
            old_string="foo",
            new_string="bar",
            allow_multiple=False,
        )
        assert result.error is not None

    def test_multiple_matches_with_allow_multiple(self, tmp_path) -> None:
        f = tmp_path / "test.py"
        f.write_text("foo\nfoo\n")
        tool = ReplaceTool()
        result = tool.execute(
            file_path=str(f),
            old_string="foo",
            new_string="bar",
            allow_multiple=True,
        )
        assert result.error is None
        assert f.read_text() == "bar\nbar\n"

    def test_file_not_found(self) -> None:
        tool = ReplaceTool()
        result = tool.execute(
            file_path="/nonexistent/file.py",
            old_string="a",
            new_string="b",
        )
        assert result.error is not None

    def test_identical_old_new(self, tmp_path) -> None:
        f = tmp_path / "test.py"
        f.write_text("hello\n")
        tool = ReplaceTool()
        result = tool.execute(
            file_path=str(f),
            old_string="hello",
            new_string="hello",
        )
        assert result.error is not None
