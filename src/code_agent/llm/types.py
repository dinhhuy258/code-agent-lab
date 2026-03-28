"""Shared types for LLM abstraction layer.

# Ref: gemini-cli ContentGenerator (packages/core/src/core/contentGenerator.ts)
# These types mirror the Gemini API's native Content format so conversion is minimal.
# Extensible for future function_call / function_response parts.
"""

from dataclasses import dataclass, field


@dataclass
class Part:
    """A single content part within a message.

    # Ref: gemini-cli uses google.genai.types.Part
    """

    text: str | None = None


@dataclass
class Content:
    """A message in the conversation history.

    # Ref: gemini-cli uses google.genai.types.Content
    """

    role: str
    parts: list[Part] = field(default_factory=list)


@dataclass
class TurnResult:
    """Result of a single LLM turn.

    # Ref: gemini-cli Turn response parsing (packages/core/src/core/turn.ts)
    """

    text: str
    finish_reason: str | None = None
    usage: dict | None = None


@dataclass
class GenerateContentRequest:
    """Request payload for LLM content generation.

    # Ref: gemini-cli GenerateContentParameters
    """

    contents: list[Content] = field(default_factory=list)
    system_instruction: str | None = None


class LLMError(Exception):
    """Unified error for LLM API failures."""
