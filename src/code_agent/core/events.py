"""Agent event types for the generator-based agent loop.

# Ref: gemini-cli ServerGeminiStreamEvent (packages/core/src/core/geminiChat.ts)
# Yielded by AgentClient.send() to report progress to the UI.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class ToolCallStart:
    """Emitted when the agent begins executing a tool call."""

    name: str
    call_id: str
    args: dict[str, Any]


@dataclass
class ToolCallEnd:
    """Emitted when a tool call finishes (success or error)."""

    name: str
    call_id: str
    error: str | None = None


@dataclass
class TextChunk:
    """Emitted when a text token arrives during streaming."""

    text: str


@dataclass
class TextResponse:
    """Emitted when the agent produces a final text response."""

    text: str


AgentEvent = ToolCallStart | ToolCallEnd | TextChunk | TextResponse
