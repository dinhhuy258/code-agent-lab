"""Turn -- a single LLM request/response cycle.

# Ref: gemini-cli Turn (packages/core/src/core/turn.ts)
# Created per request by ChatSession. Calls LLMClient and returns TurnResult.
# Future: will handle tool call extraction, streaming events.
"""

from code_agent.llm.client import LLMClient
from code_agent.llm.types import GenerateContentRequest, TurnResult


class Turn:
    """Represents a single request/response cycle with the LLM.

    # Ref: gemini-cli Turn (packages/core/src/core/turn.ts)
    """

    def run(self, client: LLMClient, request: GenerateContentRequest) -> TurnResult:
        """Execute the turn: send request to LLM and return the result.

        # Ref: gemini-cli Turn.run (packages/core/src/core/turn.ts)
        """
        return client.generate_content(request)
