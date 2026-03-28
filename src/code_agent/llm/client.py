"""LLMClient Protocol -- abstract interface for LLM API providers.

# Ref: gemini-cli ContentGenerator (packages/core/src/core/contentGenerator.ts)
# Structural typing: any class with a matching generate_content method satisfies this.
# Future: add generate_content_stream for streaming responses.
"""

from typing import Protocol

from code_agent.llm.types import GenerateContentRequest, TurnResult


class LLMClient(Protocol):
    """Protocol for LLM content generation."""

    def generate_content(self, request: GenerateContentRequest) -> TurnResult: ...
