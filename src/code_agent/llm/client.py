"""LLMClient Protocol -- abstract interface for LLM API providers.

# Structural typing: any class with a matching generate_content method satisfies this.
"""

from collections.abc import Generator
from typing import Protocol

from code_agent.llm.types import GenerateContentRequest, TurnResult


class LLMClient(Protocol):
    """Protocol for LLM content generation."""

    @property
    def model_name(self) -> str: ...

    def generate_content(self, request: GenerateContentRequest) -> TurnResult: ...

    def generate_content_stream(
        self, request: GenerateContentRequest
    ) -> Generator[TurnResult, None, None]: ...
