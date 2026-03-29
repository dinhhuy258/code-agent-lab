from code_agent.tools.shell import ShellTool


class TestShellTool:
    def test_get_name(self) -> None:
        assert ShellTool().get_name() == "run_shell_command"

    def test_needs_confirmation(self) -> None:
        assert ShellTool().needs_confirmation() is True

    def test_get_declaration(self) -> None:
        decl = ShellTool().get_declaration()
        assert "command" in decl.parameters["properties"]

    def test_run_simple_command(self) -> None:
        tool = ShellTool()
        result = tool.execute(command="echo hello")
        assert result.error is None
        assert "hello" in result.content

    def test_run_command_with_exit_code(self) -> None:
        tool = ShellTool()
        result = tool.execute(command="exit 1")
        assert result.error is not None

    def test_run_command_with_stderr(self) -> None:
        tool = ShellTool()
        result = tool.execute(command="echo error >&2 && exit 1")
        assert result.error is not None
        assert "error" in result.error

    def test_command_timeout(self) -> None:
        tool = ShellTool()
        result = tool.execute(command="sleep 60", timeout=1)
        assert result.error is not None
        assert "timed out" in result.error.lower()

    def test_empty_command(self) -> None:
        tool = ShellTool()
        result = tool.execute(command="")
        assert result.error is not None
