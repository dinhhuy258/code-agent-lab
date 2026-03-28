"""AgentClient -- top-level orchestrator with ReAct agent loop.

# Ref: gemini-cli GeminiClient (packages/core/src/core/client.ts)
# Entry point for the service layer. Owns a ChatSession and ToolRegistry.
# Implements the agent loop: call LLM -> execute tools -> repeat.
"""

from collections.abc import Callable

from code_agent.core.chat_session import ChatSession
from code_agent.llm.client import LLMClient
from code_agent.llm.types import FunctionCall
from code_agent.tools.registry import ToolRegistry

MAX_TURNS = 25


class AgentClient:
    """Orchestrates the agent loop: LLM calls, tool execution, and confirmation.

    # Ref: gemini-cli GeminiClient (packages/core/src/core/client.ts)
    """

    def __init__(
        self,
        client: LLMClient,
        tool_registry: ToolRegistry | None = None,
        system_instruction: str | None = None,
        confirm_callback: Callable[[FunctionCall], bool] | None = None,
    ) -> None:
        self._registry = tool_registry or ToolRegistry()
        self._confirm_callback = confirm_callback
        self._session = ChatSession(
            client=client,
            system_instruction=system_instruction,
            tool_declarations=self._registry.get_declarations(),
        )

    def send(self, user_text: str) -> str:
        """Send a user message and run the agent loop until a final answer.

        # Ref: gemini-cli GeminiClient.sendMessageStream
        """
        self._session.append_user_message(user_text)

        for _ in range(MAX_TURNS):
            result = self._session.send_message()

            if not result.function_calls:
                return result.text

            self._process_tool_calls(result.function_calls)

        return "Max turns reached. The agent could not complete the task within the turn limit."

    def _process_tool_calls(self, function_calls: list[FunctionCall]) -> None:
        """Execute each function call, handling confirmation and feeding results back."""
        for fc in function_calls:
            tool = self._registry.get_tool(fc.name)

            if tool and tool.needs_confirmation(**fc.args):
                if self._confirm_callback and not self._confirm_callback(fc):
                    self._session.append_function_response(fc, {"error": "User denied execution."})
                    continue

            tool_result = self._registry.execute(fc.name, **fc.args)
            if tool_result.error:
                self._session.append_function_response(fc, {"error": tool_result.error})
            else:
                self._session.append_function_response(fc, {"content": tool_result.content})
