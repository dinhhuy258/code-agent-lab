"""WriteFileTool -- write content to a file.

# Ref: gemini-cli WriteFileTool (packages/core/src/tools/write-file.ts)
"""

from pathlib import Path

from code_agent.llm.types import ToolDeclaration
from code_agent.tools.base import BaseTool, ToolResult


class WriteFileTool(BaseTool):
    """Write content to a file, creating parent directories if needed.

    # Ref: gemini-cli WriteFileTool (packages/core/src/tools/write-file.ts)
    """

    def get_name(self) -> str:
        return "write_file"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(
            name="write_file",
            description=(
                "Writes content to a specified file in the local filesystem. "
                "Creates parent directories if they don't exist."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to write to.",
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file. Provide complete literal content.",
                    },
                },
                "required": ["file_path", "content"],
            },
        )

    def needs_confirmation(self, **kwargs) -> bool:
        return True

    def execute(self, **kwargs) -> ToolResult:
        file_path: str = kwargs.get("file_path", "")
        content: str = kwargs.get("content", "")

        if not file_path:
            return ToolResult(content="", error="file_path is required.")

        path = Path(file_path)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        except OSError as e:
            return ToolResult(content="", error=f"Failed to write file: {e}")

        return ToolResult(content=f"Successfully wrote to {file_path}")
