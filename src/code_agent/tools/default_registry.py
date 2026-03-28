"""Factory for creating a ToolRegistry with all default tools.

# Ref: gemini-cli tool registration in ToolRegistry (packages/core/src/tools/tool-registry.ts)
"""

from code_agent.agents.subagent_manager import SubagentManager
from code_agent.llm.client import LLMClient
from code_agent.tools.glob import GlobTool
from code_agent.tools.grep_search import GrepSearchTool
from code_agent.tools.list_directory import ListDirectoryTool
from code_agent.tools.read_file import ReadFileTool
from code_agent.tools.registry import ToolRegistry
from code_agent.tools.replace import ReplaceTool
from code_agent.tools.shell import ShellTool
from code_agent.tools.task import TaskTool
from code_agent.tools.web_fetch import WebFetchTool
from code_agent.tools.write_file import WriteFileTool


def create_default_registry(
    llm_client: LLMClient | None = None,
    subagent_manager: SubagentManager | None = None,
) -> ToolRegistry:
    """Create a ToolRegistry with all built-in tools registered.

    Args:
        llm_client: Optional LLM client. When provided, the TaskTool (sub-agent launcher) is registered.
        subagent_manager: Optional SubagentManager. Created automatically if llm_client is provided.
    """
    registry = ToolRegistry()
    registry.register(GlobTool())
    registry.register(ReadFileTool())
    registry.register(WriteFileTool())
    registry.register(ReplaceTool())
    registry.register(ListDirectoryTool())
    registry.register(GrepSearchTool())
    registry.register(WebFetchTool())
    registry.register(ShellTool())

    if llm_client is not None:
        _subagent_manager = subagent_manager or SubagentManager()
        registry.register(TaskTool(
            llm_client=llm_client,
            tool_registry=registry,
            subagent_manager=_subagent_manager,
        ))

    return registry
