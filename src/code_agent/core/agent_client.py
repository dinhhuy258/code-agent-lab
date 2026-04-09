"""AgentClient -- top-level orchestrator with ReAct agent loop.

# Entry point for the service layer. Owns a ChatSession and ToolRegistry.
# Implements the agent loop: call LLM -> execute tools -> repeat.
# Uses generator pattern matching gemini-cli's async *sendMessageStream().
"""

from collections.abc import Generator
from typing import Any

from code_agent.core.chat_session import ChatSession
from code_agent.core.events import (
    AgentEvent,
    TextChunk,
    TextResponse,
    ToolCallEnd,
    ToolCallStart,
    ToolCallUpdate,
    UsageUpdate,
)
from code_agent.llm.client import LLMClient
from code_agent.llm.types import FunctionCall
from code_agent.tools.registry import ToolRegistry

MAX_TURNS = 25


class AgentClient:
    """Orchestrates the agent loop, yielding events for each step."""

    def __init__(
        self,
        client: LLMClient,
        tool_registry: ToolRegistry,
        system_instruction: str,
    ) -> None:
        self._registry = tool_registry
        self._session = ChatSession(
            client=client,
            system_instruction=system_instruction,
            tool_declarations=self._registry.get_declarations(),
        )

    def send(self, user_text: str) -> Generator[AgentEvent, None, None]:
        """Send a user message and run the agent loop, yielding events.

        Yields TextChunk events as tokens stream in, then TextResponse or
        ToolCallStart/End events depending on the model's response.
        """
        self._session.append_user_message(user_text)

        for _ in range(MAX_TURNS):
            final_result = None
            for result in self._session.send_message_stream():
                # Intermediate yields are text chunks (no function_calls)
                if not result.function_calls:
                    yield TextChunk(text=result.text)
                final_result = result

            if final_result is None:
                yield TextResponse(text="No response received.")
                return

            if final_result.usage:
                yield UsageUpdate(
                    prompt_token_count=final_result.usage.get("prompt_token_count", 0),
                    candidates_token_count=final_result.usage.get(
                        "candidates_token_count", 0
                    ),
                    total_token_count=final_result.usage.get("total_token_count", 0),
                    cached_content_token_count=final_result.usage.get(
                        "cached_content_token_count", 0
                    ),
                    thoughts_token_count=final_result.usage.get(
                        "thoughts_token_count", 0
                    ),
                )

            if not final_result.function_calls:
                # Stream complete with text-only response — emit final event
                yield TextResponse(text=final_result.text)
                return

            yield from self._process_tool_calls(final_result.function_calls)

        yield TextResponse(
            text="Max turns reached. The agent could not complete the task within the turn limit."
        )

    def _process_tool_calls(
        self, function_calls: list[FunctionCall]
    ) -> Generator[AgentEvent, None, None]:
        """Execute each function call, yielding start/end events."""
        for fc in function_calls:
            yield ToolCallStart(name=fc.name, call_id=fc.call_id, args=fc.args)

            # Collect live output updates in a queue
            output_queue: list[Any] = []

            def on_output(data: Any) -> None:
                output_queue.append(data)

            tool_result = self._registry.execute(
                fc.name, on_output=on_output, **fc.args
            )

            # Drain queued updates as ToolCallUpdate events
            for activities in output_queue:
                yield ToolCallUpdate(call_id=fc.call_id, activities=activities)

            if tool_result.error:
                self._session.append_function_response(fc, {"error": tool_result.error})
                yield ToolCallEnd(
                    name=fc.name, call_id=fc.call_id, error=tool_result.error
                )
            else:
                self._session.append_function_response(
                    fc, {"content": tool_result.content}
                )
                yield ToolCallEnd(name=fc.name, call_id=fc.call_id)
