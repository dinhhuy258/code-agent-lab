"""ToolRegistry -- manages tool instances and dispatches execution.

# Ref: gemini-cli ToolRegistry (packages/core/src/tools/tool-registry.ts)
"""

import logging

from code_agent.llm.types import ToolDeclaration
from code_agent.tools.base import BaseTool, ToolResult

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry of available tools.

    # Ref: gemini-cli ToolRegistry (packages/core/src/tools/tool-registry.ts)
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

    def execute(self, name: str, **kwargs) -> ToolResult:
        """Dispatch execution to the named tool.

        Returns a ToolResult with error set if the tool is unknown or execution fails.
        """
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(content="", error=f"Unknown tool: {name}")
        try:
            return tool.execute(**kwargs)
        except Exception as e:
            logger.exception("Tool '%s' raised an exception", name)
            return ToolResult(content="", error=f"Tool execution failed: {e}")
