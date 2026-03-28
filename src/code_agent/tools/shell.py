"""ShellTool -- execute shell commands.

"""

import subprocess

from code_agent.llm.types import ToolDeclaration
from code_agent.tools.base import BaseTool, ToolResult

DEFAULT_TIMEOUT = 30

class ShellTool(BaseTool):
    """Execute shell commands via subprocess.

    """

    def get_name(self) -> str:
        return "run_shell_command"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(
            name="run_shell_command",
            description=(
                "Executes a shell command and returns the output. "
                "Use this for running tests, installing packages, git operations, etc."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to execute.",
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in seconds. Defaults to 30.",
                    },
                },
                "required": ["command"],
            },
        )

    def needs_confirmation(self, **kwargs) -> bool:
        return True

    def execute(self, **kwargs) -> ToolResult:
        command: str = kwargs.get("command", "")
        timeout: int = kwargs.get("timeout", DEFAULT_TIMEOUT)

        if not command:
            return ToolResult(content="", error="command is required.")

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return ToolResult(content="", error=f"Command timed out after {timeout} seconds.")
        except OSError as e:
            return ToolResult(content="", error=f"Failed to execute command: {e}")

        if result.returncode != 0:
            error_output = result.stderr.strip() or f"Command exited with code {result.returncode}"
            return ToolResult(content=result.stdout, error=error_output)

        return ToolResult(content=result.stdout)
