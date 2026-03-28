"""TaskTool -- spawns an isolated sub-agent to handle a task.

# Ref: gemini-cli SubagentTool (packages/core/src/agents/subagent-tool.ts)
"""

import logging

from code_agent.agents.subagent_manager import SubagentManager
from code_agent.agents.subagent_runner import SubagentRunner
from code_agent.core.chat_session import ChatSession
from code_agent.llm.client import LLMClient
from code_agent.llm.types import ToolDeclaration
from code_agent.tools.base import BaseTool, ToolResult
from code_agent.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)


class TaskTool(BaseTool):
    """Spawns an isolated sub-agent to complete a task.

    # Ref: gemini-cli SubagentTool + LocalAgentExecutor
    The sub-agent gets its own ChatSession (isolated history) but shares
    the same LLMClient and ToolRegistry.
    """

    _depth: int = 0

    def __init__(
        self,
        llm_client: LLMClient,
        tool_registry: ToolRegistry,
        subagent_manager: SubagentManager,
    ) -> None:
        self._llm_client = llm_client
        self._tool_registry = tool_registry
        self._subagent_manager = subagent_manager

    def get_name(self) -> str:
        return "task"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(
            name="task",
            description=(
                "Launch a sub-agent to handle a complex task autonomously. "
                "The sub-agent runs in its own isolated context with access to the same tools. "
                "Use this for tasks that require many tool calls or would pollute the main conversation context."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "A short (3-5 word) description of the task for display purposes.",
                    },
                    "prompt": {
                        "type": "string",
                        "description": (
                            "Detailed task instructions for the sub-agent. "
                            "Must be self-contained since the sub-agent has no access to parent context."
                        ),
                    },
                    "subagent_type": {
                        "type": "string",
                        "description": "The type of sub-agent to use. Defaults to 'general-purpose'.",
                    },
                },
                "required": ["description", "prompt"],
            },
        )

    def execute(self, **kwargs) -> ToolResult:
        """Spawn a sub-agent and return its result.

        Args:
            **kwargs: Must include 'description' and 'prompt'. Optional 'subagent_type'.

        Returns:
            ToolResult with the sub-agent's response or an error.
        """
        description: str = kwargs.get("description", "")
        prompt: str = kwargs.get("prompt", "")
        subagent_type: str = kwargs.get("subagent_type", "general-purpose")

        if TaskTool._depth > 0:
            return ToolResult(content="", error="Nested sub-agents are not supported.")

        try:
            system_prompt = self._subagent_manager.get_prompt(subagent_type)
        except ValueError as e:
            return ToolResult(content="", error=str(e))

        try:
            TaskTool._depth += 1

            session = ChatSession(
                client=self._llm_client,
                system_instruction=system_prompt,
                tool_declarations=self._tool_registry.get_declarations(),
            )
            runner = SubagentRunner(
                chat_session=session,
                tool_registry=self._tool_registry,
            )

            logger.info("Sub-agent started: %s (type=%s)", description, subagent_type)
            response = runner.run(prompt)
            logger.info("Sub-agent finished: %s", description)

            return ToolResult(content=f"Task Finished with response: {response}")
        except Exception as e:
            logger.exception("Sub-agent failed: %s", description)
            return ToolResult(content="", error=f"Sub-agent failed: {e}")
        finally:
            TaskTool._depth -= 1
