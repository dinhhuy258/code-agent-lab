"""ListDirectoryTool -- list files and subdirectories."""

from pathlib import Path

from code_agent.llm.types import ToolDeclaration
from code_agent.tools.base import BaseTool, ToolResult


class ListDirectoryTool(BaseTool):
    """List the names of files and subdirectories within a directory."""

    def get_name(self) -> str:
        return "list_directory"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(
            name="list_directory",
            description="Lists the names of files and subdirectories directly within a specified directory path.",
            parameters={
                "type": "object",
                "properties": {
                    "dir_path": {
                        "type": "string",
                        "description": "The path to the directory to list.",
                    },
                },
                "required": ["dir_path"],
            },
        )

    def execute(self, **kwargs) -> ToolResult:
        dir_path: str = kwargs.get("dir_path", ".")

        path = Path(dir_path)
        if not path.exists():
            return ToolResult(content="", error=f"Directory does not exist: {dir_path}")
        if not path.is_dir():
            return ToolResult(content="", error=f"Path is not a directory: {dir_path}")

        entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        lines = []
        for entry in entries:
            if entry.is_dir():
                lines.append(f"[DIR] {entry.name}")
            else:
                size = entry.stat().st_size
                lines.append(f"{entry.name} ({size} bytes)")

        if not lines:
            return ToolResult(content="Empty directory.")

        return ToolResult(content="\n".join(lines))
