"""ReadFileTool -- read file contents with optional line range."""

from pathlib import Path

from code_agent.llm.types import ToolDeclaration
from code_agent.tools.base import BaseTool, ToolResult

MAX_READ_SIZE = 100_000  # ~100KB


class ReadFileTool(BaseTool):
    """Read the content of a file, optionally within a line range."""

    def get_name(self) -> str:
        return "read_file"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(
            name="read_file",
            description=(
                "Reads and returns the content of a specified file. "
                "If the file is large, the content will be truncated. "
                "For text files, it can read specific line ranges using start_line and end_line."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read.",
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "The 1-based line number to start reading from.",
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "The 1-based line number to end reading at (inclusive).",
                    },
                },
                "required": ["file_path"],
            },
        )

    def execute(self, **kwargs) -> ToolResult:
        file_path: str = kwargs.get("file_path", "")
        start_line: int | None = kwargs.get("start_line")
        end_line: int | None = kwargs.get("end_line")

        path = Path(file_path)
        if not path.exists():
            return ToolResult(content="", error=f"File not found: {file_path}")
        if not path.is_file():
            return ToolResult(content="", error=f"Path is not a file: {file_path}")

        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as e:
            return ToolResult(content="", error=f"Failed to read file: {e}")

        if start_line is not None or end_line is not None:
            s = (start_line or 1) - 1
            e = end_line or len(lines)
            selected = lines[s:e]
            numbered = [f"{i + s + 1}:\t{line}" for i, line in enumerate(selected)]
        else:
            numbered = [f"{i + 1}:\t{line}" for i, line in enumerate(lines)]

        content = "\n".join(numbered)
        truncated = False
        if len(content) > MAX_READ_SIZE:
            content = content[:MAX_READ_SIZE]
            truncated = True

        if truncated:
            content += f"\n\n[Truncated at {MAX_READ_SIZE} characters. Use start_line/end_line to read specific sections.]"

        return ToolResult(content=content)
