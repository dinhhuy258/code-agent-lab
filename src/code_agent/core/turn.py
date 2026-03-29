"""Turn -- a single LLM request/response cycle.

# Created per request by ChatSession. Calls LLMClient and returns TurnResult.
"""

from collections.abc import Generator

from code_agent.llm.client import LLMClient
from code_agent.llm.types import GenerateContentRequest, TurnResult


class Turn:
    """Represents a single request/response cycle with the LLM."""

    def run(self, client: LLMClient, request: GenerateContentRequest) -> TurnResult:
        """Execute the turn: send request to LLM and return the result."""
        return client.generate_content(request)

    def run_stream(
        self, client: LLMClient, request: GenerateContentRequest
    ) -> Generator[TurnResult, None, None]:
        """Execute the turn with streaming, yielding partial TurnResults.

        Intermediate yields contain text chunks only. The final yield
        contains the complete text and any function calls.
        """
        yield from client.generate_content_stream(request)
