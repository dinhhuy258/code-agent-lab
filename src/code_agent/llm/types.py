"""Shared types for LLM abstraction layer.

# These types mirror the Gemini API's native Content format so conversion is minimal.
"""

from dataclasses import dataclass, field
from typing import Any

@dataclass
class FunctionCall:
    """A function call requested by the model.

    """

    name: str
    args: dict[str, Any]
    call_id: str

@dataclass
class FunctionResponse:
    """A function response to send back to the model.

    """

    name: str
    call_id: str
    response: dict[str, Any]

@dataclass
class ToolDeclaration:
    """Schema declaration for a tool to send to the LLM API.

    """

    name: str
    description: str
    parameters: dict[str, Any]

@dataclass
class Part:
    """A single content part within a message.

    """

    text: str | None = None
    function_call: FunctionCall | None = None
    function_response: FunctionResponse | None = None

@dataclass
class Content:
    """A message in the conversation history.

    """

    role: str
    parts: list[Part] = field(default_factory=list)

@dataclass
class TurnResult:
    """Result of a single LLM turn.

    """

    text: str
    function_calls: list[FunctionCall] = field(default_factory=list)
    finish_reason: str | None = None
    usage: dict | None = None

@dataclass
class GenerateContentRequest:
    """Request payload for LLM content generation.

    """

    contents: list[Content] = field(default_factory=list)
    system_instruction: str | None = None
    tools: list[ToolDeclaration] = field(default_factory=list)

class LLMError(Exception):
    """Unified error for LLM API failures."""
