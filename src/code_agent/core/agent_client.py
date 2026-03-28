"""AgentClient -- top-level orchestrator for chat interactions.

# Ref: gemini-cli GeminiClient (packages/core/src/core/client.ts)
# Entry point for the service layer. Owns a ChatSession.
# Future: agent loop, turn limits, hook system.
"""

from code_agent.core.chat_session import ChatSession
from code_agent.llm.client import LLMClient


class AgentClient:
    """Orchestrates chat interactions via ChatSession.

    # Ref: gemini-cli GeminiClient (packages/core/src/core/client.ts)
    """

    def __init__(
        self,
        client: LLMClient,
        system_instruction: str | None = None,
    ) -> None:
        self._session = ChatSession(
            client=client,
            system_instruction=system_instruction,
        )

    def send(self, user_text: str) -> str:
        """Send a user message and return the LLM response.

        # Ref: gemini-cli GeminiClient.sendMessageStream
        """
        return self._session.send_message(user_text)
