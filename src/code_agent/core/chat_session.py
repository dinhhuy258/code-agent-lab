"""ChatSession -- manages conversation history and request building.

# Ref: gemini-cli GeminiChat (packages/core/src/core/geminiChat.ts)
# Owns the conversation history. Creates Turn instances for each request.
"""

from typing import Any

from code_agent.core.turn import Turn
from code_agent.llm.client import LLMClient
from code_agent.llm.types import (
    Content,
    FunctionCall,
    FunctionResponse,
    GenerateContentRequest,
    LLMError,
    Part,
    ToolDeclaration,
    TurnResult,
)


class ChatSession:
    """Manages conversation history and delegates to Turn for LLM calls.

    # Ref: gemini-cli GeminiChat (packages/core/src/core/geminiChat.ts)
    """

    def __init__(
        self,
        client: LLMClient,
        system_instruction: str | None = None,
        tool_declarations: list[ToolDeclaration] | None = None,
    ) -> None:
        self._client = client
        self._system_instruction = system_instruction
        self._tool_declarations = tool_declarations or []
        self._history: list[Content] = []

    def append_user_message(self, user_text: str) -> None:
        """Append a user text message to the conversation history."""
        self._history.append(Content(role="user", parts=[Part(text=user_text)]))

    def append_function_response(self, function_call: FunctionCall, response: dict[str, Any]) -> None:
        """Append a function response to the conversation history.

        # Ref: gemini-cli sends function_response as user role content
        """
        self._history.append(
            Content(
                role="user",
                parts=[
                    Part(
                        function_response=FunctionResponse(
                            name=function_call.name,
                            call_id=function_call.call_id,
                            response=response,
                        )
                    )
                ],
            )
        )

    def send_message(self) -> TurnResult:
        """Send the current history to the LLM and return the result.

        Appends the model's response to history on success.

        # Ref: gemini-cli GeminiChat.sendMessageStream
        """
        request = GenerateContentRequest(
            contents=list(self._history),
            system_instruction=self._system_instruction,
            tools=self._tool_declarations,
        )

        turn = Turn()
        try:
            result = turn.run(self._client, request)
        except LLMError as e:
            return TurnResult(text=f"Error: {e}")

        self._append_model_response(result)
        return result

    def get_history(self) -> list[Content]:
        """Return the full conversation history.

        # Ref: gemini-cli GeminiChat.getHistory
        """
        return list(self._history)

    def _append_model_response(self, result: TurnResult) -> None:
        """Append the model's response parts to history."""
        parts: list[Part] = []
        if result.function_calls:
            for fc in result.function_calls:
                parts.append(Part(function_call=fc))
        if result.text:
            parts.append(Part(text=result.text))
        if not parts:
            parts.append(Part(text=""))
        self._history.append(Content(role="model", parts=parts))
