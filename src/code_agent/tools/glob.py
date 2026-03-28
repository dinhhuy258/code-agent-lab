"""GlobTool -- find files matching glob patterns.

"""

import glob as glob_module
from pathlib import Path

from code_agent.llm.types import ToolDeclaration
from code_agent.tools.base import BaseTool, ToolResult

class GlobTool(BaseTool):
    """Find files matching glob patterns, sorted by modification time.

    """

    def get_name(self) -> str:
        return "glob"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(
            name="glob",
            description=(
                "Efficiently finds files matching specific glob patterns (e.g., 'src/**/*.ts', '**/*.md'), "
                "returning paths sorted by modification time (newest first). "
                "Ideal for quickly locating files based on their name or path structure."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "The glob pattern to match against (e.g., '**/*.py', 'docs/*.md').",
                    },
                    "dir_path": {
                        "type": "string",
                        "description": "The absolute path to the directory to search within. Defaults to current working directory.",
                    },
                },
                "required": ["pattern"],
            },
        )

    def execute(self, **kwargs) -> ToolResult:
        pattern: str = kwargs.get("pattern", "")
        dir_path: str = kwargs.get("dir_path", ".")

        search_dir = Path(dir_path)
        if not search_dir.exists():
            return ToolResult(content="", error=f"Directory does not exist: {dir_path}")
        if not search_dir.is_dir():
            return ToolResult(content="", error=f"Path is not a directory: {dir_path}")

        full_pattern = str(search_dir / pattern)
        matches = glob_module.glob(full_pattern, recursive=True)
        files = [m for m in matches if Path(m).is_file()]
        files.sort(key=lambda f: Path(f).stat().st_mtime, reverse=True)

        if not files:
            return ToolResult(content=f"No files found matching pattern '{pattern}' in {dir_path}")

        result_lines = [f"Found {len(files)} file(s):"]
        result_lines.extend(files)
        return ToolResult(content="\n".join(result_lines))
