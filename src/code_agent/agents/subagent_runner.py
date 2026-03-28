"""SubagentRunner -- runs an isolated ReAct loop to completion.

# Ref: gemini-cli LocalAgentExecutor (packages/core/src/agents/local-executor.ts)
# Simplified version: no streaming events, no recovery turns, sequential only.
"""

import logging

from code_agent.core.chat_session import ChatSession
from code_agent.llm.types import FunctionCall
from code_agent.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)

DEFAULT_MAX_TURNS = 15


class SubagentRunner:
    """Runs an isolated ReAct loop and returns the final text response.

    # Ref: gemini-cli LocalAgentExecutor.run()
    Unlike AgentClient, this does not yield events -- it runs silently and
    returns a string. It exits when the LLM responds without tool calls.
    """

    def __init__(
        self,
        chat_session: ChatSession,
        tool_registry: ToolRegistry,
        max_turns: int = DEFAULT_MAX_TURNS,
    ) -> None:
        self._session = chat_session
        self._registry = tool_registry
        self._max_turns = max_turns

    def run(self, prompt: str) -> str:
        """Run the sub-agent loop and return the final text response.

        Args:
            prompt: The task prompt to send to the sub-agent.

        Returns:
            The sub-agent's final text response.
        """
        self._session.append_user_message(prompt)

        final_result = None
        for _turn in range(self._max_turns):
            for result in self._session.send_message_stream():
                final_result = result

            if final_result is None:
                return "Sub-agent received no response from the model."

            if not final_result.function_calls:
                return final_result.text

            self._process_tool_calls(final_result.function_calls)

        last_text = final_result.text if final_result else "none"
        return f"Sub-agent reached turn limit ({self._max_turns}). Last response: {last_text}"

    def _process_tool_calls(self, function_calls: list[FunctionCall]) -> None:
        """Execute tool calls and append responses to the session history."""
        for fc in function_calls:
            tool_result = self._registry.execute(fc.name, **fc.args)
            if tool_result.error:
                self._session.append_function_response(fc, {"error": tool_result.error})
            else:
                self._session.append_function_response(fc, {"content": tool_result.content})
