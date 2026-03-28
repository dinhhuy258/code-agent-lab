"""ReplaceTool -- find-and-replace text in files.

# Ref: gemini-cli EditTool (packages/core/src/tools/edit.ts)
"""

from pathlib import Path

from code_agent.llm.types import ToolDeclaration
from code_agent.tools.base import BaseTool, ToolResult


class ReplaceTool(BaseTool):
    """Find and replace exact text in a file.

    # Ref: gemini-cli EditTool (packages/core/src/tools/edit.ts)
    """

    def get_name(self) -> str:
        return "replace"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(
            name="replace",
            description=(
                "Replaces exact literal text in a file. "
                "The old_string must match exactly (including whitespace and indentation). "
                "Include at least 3 lines of context before and after the target text."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to modify.",
                    },
                    "old_string": {
                        "type": "string",
                        "description": "The exact literal text to replace. Must match exactly including whitespace.",
                    },
                    "new_string": {
                        "type": "string",
                        "description": "The exact literal text to replace old_string with.",
                    },
                    "allow_multiple": {
                        "type": "boolean",
                        "description": "If true, replace all occurrences. If false (default), only succeed if exactly one occurrence is found.",
                    },
                },
                "required": ["file_path", "old_string", "new_string"],
            },
        )

    def needs_confirmation(self, **kwargs) -> bool:
        return True

    def execute(self, **kwargs) -> ToolResult:
        file_path: str = kwargs.get("file_path", "")
        old_string: str = kwargs.get("old_string", "")
        new_string: str = kwargs.get("new_string", "")
        allow_multiple: bool = kwargs.get("allow_multiple", False)

        if not file_path:
            return ToolResult(content="", error="file_path is required.")

        if old_string == new_string:
            return ToolResult(content="", error="old_string and new_string are identical. No change needed.")

        path = Path(file_path)
        if not path.exists():
            return ToolResult(content="", error=f"File not found: {file_path}")
        if not path.is_file():
            return ToolResult(content="", error=f"Path is not a file: {file_path}")

        try:
            content = path.read_text(encoding="utf-8")
        except OSError as e:
            return ToolResult(content="", error=f"Failed to read file: {e}")

        count = content.count(old_string)
        if count == 0:
            return ToolResult(content="", error=f"No occurrences of old_string found in {file_path}.")

        if not allow_multiple and count > 1:
            return ToolResult(
                content="",
                error=f"Found {count} occurrences of old_string, but allow_multiple is false. Use allow_multiple=true or provide more context to uniquely identify the target.",
            )

        new_content = content.replace(old_string, new_string)
        try:
            path.write_text(new_content, encoding="utf-8")
        except OSError as e:
            return ToolResult(content="", error=f"Failed to write file: {e}")

        replacements = "all occurrences" if allow_multiple else "1 occurrence"
        return ToolResult(content=f"Replaced {replacements} in {file_path}.")
