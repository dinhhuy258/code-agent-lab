"""Turn -- a single LLM request/response cycle.

# Ref: gemini-cli Turn (packages/core/src/core/turn.ts)
# Created per request by ChatSession. Calls LLMClient and returns TurnResult.
"""

from collections.abc import Generator

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

    def run_stream(self, client: LLMClient, request: GenerateContentRequest) -> Generator[TurnResult, None, None]:
        """Execute the turn with streaming, yielding partial TurnResults.

        # Ref: gemini-cli Turn.run (packages/core/src/core/turn.ts)
        Intermediate yields contain text chunks only. The final yield
        contains the complete text and any function calls.
        """
        yield from client.generate_content_stream(request)
