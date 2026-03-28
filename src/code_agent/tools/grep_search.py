"""GrepSearchTool -- search file contents with regex patterns.

# Ref: gemini-cli RipGrepTool (packages/core/src/tools/ripGrep.ts)
# Uses subprocess to call grep/rg for performance.
"""

import re
import subprocess
from pathlib import Path

from code_agent.llm.types import ToolDeclaration
from code_agent.tools.base import BaseTool, ToolResult

DEFAULT_MAX_MATCHES = 100


class GrepSearchTool(BaseTool):
    """Search for a regex pattern within file contents.

    # Ref: gemini-cli RipGrepTool (packages/core/src/tools/ripGrep.ts)
    """

    def get_name(self) -> str:
        return "grep_search"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(
            name="grep_search",
            description=(
                "Searches for a regular expression pattern within file contents. "
                "Returns matching lines with file paths and line numbers."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "The regex pattern to search for.",
                    },
                    "dir_path": {
                        "type": "string",
                        "description": "Directory to search recursively. Defaults to current working directory.",
                    },
                    "include_pattern": {
                        "type": "string",
                        "description": "Glob pattern to filter files (e.g., '*.py'). Defaults to all files.",
                    },
                    "case_sensitive": {
                        "type": "boolean",
                        "description": "Whether search is case-sensitive. Defaults to true.",
                    },
                },
                "required": ["pattern"],
            },
        )

    def execute(self, **kwargs) -> ToolResult:
        pattern: str = kwargs.get("pattern", "")
        dir_path: str = kwargs.get("dir_path", ".")
        include_pattern: str | None = kwargs.get("include_pattern")
        case_sensitive: bool = kwargs.get("case_sensitive", True)

        search_dir = Path(dir_path)
        if not search_dir.exists():
            return ToolResult(content="", error=f"Directory does not exist: {dir_path}")

        cmd = ["grep", "-rn"]
        if not case_sensitive:
            cmd.append("-i")
        if include_pattern:
            cmd.extend(["--include", include_pattern])
        cmd.extend([pattern, str(search_dir)])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            return ToolResult(content="", error="Search timed out after 30 seconds.")
        except FileNotFoundError:
            return self._fallback_grep(pattern, search_dir, include_pattern, case_sensitive)

        if result.returncode == 1:
            return ToolResult(content=f"No matches found for pattern '{pattern}'.")
        if result.returncode != 0:
            return ToolResult(content="", error=f"grep failed: {result.stderr.strip()}")

        lines = result.stdout.strip().splitlines()
        if len(lines) > DEFAULT_MAX_MATCHES:
            lines = lines[:DEFAULT_MAX_MATCHES]
            lines.append(f"\n[Truncated to {DEFAULT_MAX_MATCHES} matches.]")

        return ToolResult(content="\n".join(lines))

    def _fallback_grep(
        self,
        pattern: str,
        search_dir: Path,
        include_pattern: str | None,
        case_sensitive: bool,
    ) -> ToolResult:
        """Pure-Python fallback when grep is not available."""
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            regex = re.compile(pattern, flags)
        except re.error as e:
            return ToolResult(content="", error=f"Invalid regex pattern: {e}")

        matches = []
        glob_pattern = include_pattern or "**/*"
        for file_path in search_dir.glob(glob_pattern):
            if not file_path.is_file():
                continue
            try:
                lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for line_num, line in enumerate(lines, 1):
                if regex.search(line):
                    matches.append(f"{file_path}:{line_num}:{line}")
                    if len(matches) >= DEFAULT_MAX_MATCHES:
                        matches.append(f"\n[Truncated to {DEFAULT_MAX_MATCHES} matches.]")
                        return ToolResult(content="\n".join(matches))

        if not matches:
            return ToolResult(content=f"No matches found for pattern '{pattern}'.")

        return ToolResult(content="\n".join(matches))
