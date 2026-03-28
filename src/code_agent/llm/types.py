"""Shared types for LLM abstraction layer.

# Ref: gemini-cli ContentGenerator (packages/core/src/core/contentGenerator.ts)
# These types mirror the Gemini API's native Content format so conversion is minimal.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FunctionCall:
    """A function call requested by the model.

    # Ref: gemini-cli google.genai.types.FunctionCall
    """

    name: str
    args: dict[str, Any]
    call_id: str


@dataclass
class FunctionResponse:
    """A function response to send back to the model.

    # Ref: gemini-cli google.genai.types.FunctionResponse
    """

    name: str
    call_id: str
    response: dict[str, Any]


@dataclass
class ToolDeclaration:
    """Schema declaration for a tool to send to the LLM API.

    # Ref: gemini-cli FunctionDeclaration (packages/core/src/tools/definitions/)
    """

    name: str
    description: str
    parameters: dict[str, Any]


@dataclass
class Part:
    """A single content part within a message.

    # Ref: gemini-cli uses google.genai.types.Part
    """

    text: str | None = None
    function_call: FunctionCall | None = None
    function_response: FunctionResponse | None = None


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
    function_calls: list[FunctionCall] = field(default_factory=list)
    finish_reason: str | None = None
    usage: dict | None = None


@dataclass
class GenerateContentRequest:
    """Request payload for LLM content generation.

    # Ref: gemini-cli GenerateContentParameters
    """

    contents: list[Content] = field(default_factory=list)
    system_instruction: str | None = None
    tools: list[ToolDeclaration] = field(default_factory=list)


class LLMError(Exception):
    """Unified error for LLM API failures."""
