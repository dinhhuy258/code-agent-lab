"""ChatSession -- manages conversation history and request building.

# Ref: gemini-cli GeminiChat (packages/core/src/core/geminiChat.ts)
# Owns the conversation history. Creates Turn instances for each request.
# Future: history compression, token counting.
"""

from code_agent.core.turn import Turn
from code_agent.llm.client import LLMClient
from code_agent.llm.types import (
    Content,
    GenerateContentRequest,
    LLMError,
    Part,
)


class ChatSession:
    """Manages conversation history and delegates to Turn for LLM calls.

    # Ref: gemini-cli GeminiChat (packages/core/src/core/geminiChat.ts)
    """

    def __init__(
        self,
        client: LLMClient,
        system_instruction: str | None = None,
    ) -> None:
        self._client = client
        self._system_instruction = system_instruction
        self._history: list[Content] = []

    def send_message(self, user_text: str) -> str:
        """Append user message to history, run a Turn, return response text.

        # Ref: gemini-cli GeminiChat.sendMessageStream
        """
        user_content = Content(role="user", parts=[Part(text=user_text)])
        self._history.append(user_content)

        request = GenerateContentRequest(
            contents=list(self._history),
            system_instruction=self._system_instruction,
        )

        turn = Turn()
        try:
            result = turn.run(self._client, request)
        except LLMError as e:
            return f"Error: {e}"

        model_content = Content(role="model", parts=[Part(text=result.text)])
        self._history.append(model_content)

        return result.text

    def get_history(self) -> list[Content]:
        """Return the full conversation history.

        # Ref: gemini-cli GeminiChat.getHistory
        """
        return list(self._history)
