"""Agent event types for the generator-based agent loop.

# Yielded by AgentClient.send() to report progress to the UI.
"""

from dataclasses import dataclass, field
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
class SubagentActivity:
    """A single activity item from a running sub-agent.

    """

    type: str
    name: str
    status: str
    args: str = ""

@dataclass
class ToolCallUpdate:
    """Emitted when a long-running tool has intermediate progress.

    """

    call_id: str
    activities: list[SubagentActivity] = field(default_factory=list)

@dataclass
class TextChunk:
    """Emitted when a text token arrives during streaming."""

    text: str

@dataclass
class TextResponse:
    """Emitted when the agent produces a final text response."""

    text: str

@dataclass
class UsageUpdate:
    """Emitted after each LLM turn with token usage data."""

    prompt_token_count: int
    candidates_token_count: int
    total_token_count: int
    cached_content_token_count: int = 0
    thoughts_token_count: int = 0

AgentEvent = ToolCallStart | ToolCallEnd | ToolCallUpdate | TextChunk | TextResponse | UsageUpdate
