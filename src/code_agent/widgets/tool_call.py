"""ToolCallMessage -- compact one-liner showing tool execution status.

# Ref: gemini-cli ToolMessage (packages/cli/src/ui/components/messages/ToolMessage.tsx)
# Ref: gemini-cli ToolShared (packages/cli/src/ui/components/messages/ToolShared.tsx)
"""

from typing import Any

from textual.widgets import Static

MAX_ARG_VALUE_LEN = 60
MAX_TOTAL_ARGS_LEN = 120


class ToolCallMessage(Static):
    """Displays a compact one-liner for a tool call with status indicator.

    While executing: spinner read_file file_path=app.py
    On success:      checkmark read_file file_path=app.py
    On error:        x read_file file_path=app.py
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
        self.update(display)

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
