"""BaseTool ABC and ToolResult dataclass.

# Ref: gemini-cli BaseDeclarativeTool (packages/core/src/tools/tools.ts)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from code_agent.llm.types import ToolDeclaration


@dataclass
class ToolResult:
    """Result of a tool execution.

    # Ref: gemini-cli ToolResult (packages/core/src/tools/tools.ts)
    """

    content: str
    error: str | None = None


class BaseTool(ABC):
    """Abstract base class for all tools.

    # Ref: gemini-cli BaseDeclarativeTool (packages/core/src/tools/tools.ts)
    """

    @abstractmethod
    def get_name(self) -> str:
        """Return the unique tool name for dispatch."""

    @abstractmethod
    def get_declaration(self) -> ToolDeclaration:
        """Return the tool schema declaration for the LLM API."""

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with the given arguments."""

    def needs_confirmation(self, **kwargs) -> bool:
        """Return True if this tool invocation requires user approval.

        Override in subclasses for dangerous operations.
        """
        return False
