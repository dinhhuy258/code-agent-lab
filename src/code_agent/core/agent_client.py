"""AgentClient -- top-level orchestrator with ReAct agent loop.

# Ref: gemini-cli GeminiClient (packages/core/src/core/client.ts)
# Entry point for the service layer. Owns a ChatSession and ToolRegistry.
# Implements the agent loop: call LLM -> execute tools -> repeat.
# Uses generator pattern matching gemini-cli's async *sendMessageStream().
"""

from collections.abc import Callable, Generator

from code_agent.core.chat_session import ChatSession
from code_agent.core.events import AgentEvent, TextResponse, ToolCallEnd, ToolCallStart
from code_agent.llm.client import LLMClient
from code_agent.llm.types import FunctionCall
from code_agent.tools.registry import ToolRegistry

MAX_TURNS = 25


class AgentClient:
    """Orchestrates the agent loop, yielding events for each step.

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

    def send(self, user_text: str) -> Generator[AgentEvent, None, None]:
        """Send a user message and run the agent loop, yielding events.

        # Ref: gemini-cli GeminiClient.sendMessageStream
        """
        self._session.append_user_message(user_text)

        for _ in range(MAX_TURNS):
            result = self._session.send_message()

            if not result.function_calls:
                yield TextResponse(text=result.text)
                return

            yield from self._process_tool_calls(result.function_calls)

        yield TextResponse(text="Max turns reached. The agent could not complete the task within the turn limit.")

    def _process_tool_calls(self, function_calls: list[FunctionCall]) -> Generator[AgentEvent, None, None]:
        """Execute each function call, yielding start/end events."""
        for fc in function_calls:
            yield ToolCallStart(name=fc.name, call_id=fc.call_id, args=fc.args)

            tool = self._registry.get_tool(fc.name)

            if tool and tool.needs_confirmation(**fc.args):
                if self._confirm_callback and not self._confirm_callback(fc):
                    self._session.append_function_response(fc, {"error": "User denied execution."})
                    yield ToolCallEnd(name=fc.name, call_id=fc.call_id, error="User denied execution.")
                    continue

            tool_result = self._registry.execute(fc.name, **fc.args)
            if tool_result.error:
                self._session.append_function_response(fc, {"error": tool_result.error})
                yield ToolCallEnd(name=fc.name, call_id=fc.call_id, error=tool_result.error)
            else:
                self._session.append_function_response(fc, {"content": tool_result.content})
                yield ToolCallEnd(name=fc.name, call_id=fc.call_id)
