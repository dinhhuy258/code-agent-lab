"""ToolRegistry -- manages tool instances and dispatches execution.

"""

import logging
from collections.abc import Callable
from typing import Any

from code_agent.llm.types import ToolDeclaration
from code_agent.tools.base import BaseTool, ToolResult

logger = logging.getLogger(__name__)

OnOutputCallback = Callable[[Any], None]

class ToolRegistry:
    """Registry of available tools.

    """

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool instance."""
        self._tools[tool.get_name()] = tool

    def get_tool(self, name: str) -> BaseTool | None:
        """Look up a tool by name."""
        return self._tools.get(name)

    def get_declarations(self) -> list[ToolDeclaration]:
        """Return all tool schema declarations for the LLM API."""
        return [tool.get_declaration() for tool in self._tools.values()]

    def execute(
        self,
        name: str,
        on_output: OnOutputCallback | None = None,
        **kwargs,
    ) -> ToolResult:
        """Dispatch execution to the named tool.

        Args:
            name: The tool name to execute.
            on_output: Optional callback for tools that produce live output (e.g. TaskTool).
            **kwargs: Arguments to pass to the tool.

        Returns:
            ToolResult with error set if the tool is unknown or execution fails.
        """
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(content="", error=f"Unknown tool: {name}")
        try:
            if on_output is not None:
                kwargs["on_output"] = on_output
            return tool.execute(**kwargs)
        except Exception as e:
            logger.exception("Tool '%s' raised an exception", name)
            return ToolResult(content="", error=f"Tool execution failed: {e}")
