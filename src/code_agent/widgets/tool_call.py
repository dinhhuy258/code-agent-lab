"""ToolCallMessage -- compact one-liner showing tool execution status.

"""

from __future__ import annotations

from typing import Any

from textual.widgets import Static

from code_agent.core.events import SubagentActivity

MAX_ARG_VALUE_LEN = 60
MAX_TOTAL_ARGS_LEN = 120

class ToolCallMessage(Static):
    """Displays a compact one-liner for a tool call with status indicator.

    While executing: spinner read_file file_path=app.py
    On success:      checkmark read_file file_path=app.py
    On error:        x read_file file_path=app.py

    For sub-agent tool calls, also displays recent activity lines:
      spinner task description="Search for auth"
        checkmark grep_search
        checkmark read_file
        spinner read_file
    """

    DEFAULT_CSS = """
    ToolCallMessage {
        margin: 0 2 0 2;
        padding: 0 1;
        color: $text-muted;
    }
    """

    SPINNER_FRAMES = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")
    SUCCESS_SYMBOL = "✓"
    ERROR_SYMBOL = "✗"

    def __init__(self, name: str, args: dict[str, Any]) -> None:
        self._tool_name = name
        self._args = args
        self._is_complete = False
        self._error: str | None = None
        self._frame = 0
        self._activities: list[SubagentActivity] = []
        formatted = self._format_args()
        display = f"{self.SPINNER_FRAMES[0]} {name}"
        if formatted:
            display += f" {formatted}"
        super().__init__(display)

    def on_mount(self) -> None:
        """Start the spinner animation."""
        self.set_interval(0.1, self._tick)

    def _tick(self) -> None:
        """Advance the spinner frame."""
        if self._is_complete:
            return
        self._frame = (self._frame + 1) % len(self.SPINNER_FRAMES)
        self._render_display()

    def mark_complete(self, error: str | None = None) -> None:
        """Mark this tool call as complete (success or error)."""
        self._is_complete = True
        self._error = error
        self._render_display()

    def update_activities(self, activities: list[SubagentActivity]) -> None:
        """Update the sub-agent activity lines displayed below the main tool call.

        """
        self._activities = activities
        self._render_display()

    def _render_display(self) -> None:
        """Update the displayed text based on current state."""
        if self._is_complete:
            symbol = self.ERROR_SYMBOL if self._error else self.SUCCESS_SYMBOL
        else:
            symbol = self.SPINNER_FRAMES[self._frame]

        formatted = self._format_args()
        display = f"{symbol} {self._tool_name}"
        if formatted:
            display += f" {formatted}"

        for activity in self._activities:
            activity_symbol = self._activity_symbol(activity.status)
            display += f"\n  {activity_symbol} {activity.name}"

        self.update(display)

    @staticmethod
    def _activity_symbol(status: str) -> str:
        """Return the display symbol for a sub-agent activity status."""
        if status == "completed":
            return ToolCallMessage.SUCCESS_SYMBOL
        if status == "error":
            return ToolCallMessage.ERROR_SYMBOL
        return ToolCallMessage.SPINNER_FRAMES[0]

    def _format_args(self) -> str:
        """Format tool arguments as a compact key=value string."""
        if not self._args:
            return ""

        parts = []
        total_len = 0
        for key, value in self._args.items():
            value_str = str(value)
            if len(value_str) > MAX_ARG_VALUE_LEN:
                value_str = value_str[:MAX_ARG_VALUE_LEN - 3] + "..."
            part = f"{key}={value_str}"
            if total_len + len(part) > MAX_TOTAL_ARGS_LEN:
                parts.append("...")
                break
            parts.append(part)
            total_len += len(part) + 1

        return " ".join(parts)
