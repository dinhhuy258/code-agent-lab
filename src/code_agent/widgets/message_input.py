"""MessageInput -- multi-line text input with enter to submit, shift+enter for newlines."""

from textual.document._document import Location
from textual.events import Key
from textual.message import Message
from textual.widgets import TextArea


class MessageInput(TextArea):
    """Multi-line input with bordered card style. Enter submits, Shift+Enter adds newline."""

    DEFAULT_CSS = """
    MessageInput {
        height: auto;
        max-height: 10;
        min-height: 3;
        margin: 0 1 0 1;
        border: round $primary;
        border-title-color: $primary;
        border-title-style: bold;
        border-subtitle-color: $text-muted;
        padding: 0 1;
    }
    MessageInput:focus {
        border: round $accent;
        border-title-color: $accent;
    }
    """

    class Submitted(Message):
        """Posted when the user presses enter to submit."""

        def __init__(self, text: str) -> None:
            super().__init__()
            self.text = text

    def __init__(self) -> None:
        super().__init__(
            language=None,
            soft_wrap=True,
            show_line_numbers=False,
            tab_behavior="focus",
            compact=True,
        )
        self.border_title = "Message"
        self.border_subtitle = "\\ + enter for newline"

    async def _on_key(self, event: Key) -> None:
        """Intercept enter: submit normally, or insert newline if preceded by backslash."""
        if event.key == "enter":
            event.prevent_default()
            event.stop()
            if self.text.endswith("\\"):
                # Delete the trailing backslash at cursor position, then insert newline
                row, col = self.cursor_location
                start: Location = (row, col - 1)
                end: Location = (row, col)
                self.delete(start, end)
                self.insert("\n")
            else:
                text = self.text.strip()
                if not text:
                    return
                self.post_message(self.Submitted(text))
                self.clear()
        else:
            await super()._on_key(event)
