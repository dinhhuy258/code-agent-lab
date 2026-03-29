from textual.widgets import Markdown, Static


class UserMessage(Static):
    """Displays a user message in a bordered card."""

    DEFAULT_CSS = """
    UserMessage {
        margin: 1 1 0 1;
        padding: 1 2;
        border: round $primary;
        border-title-color: $primary;
        border-title-style: bold;
        background: $primary 8%;
    }
    """

    def __init__(self, content: str) -> None:
        super().__init__(content, classes="user-message")
        self.border_title = "You"


class AgentMessage(Markdown):
    """Displays an agent response with markdown rendering in a bordered card."""

    DEFAULT_CSS = """
    AgentMessage {
        margin: 1 1 0 1;
        padding: 1 2;
        border: round $accent;
        border-title-color: $accent;
        border-title-style: bold;
        background: $accent 8%;
    }
    """

    def __init__(self, content: str = "") -> None:
        super().__init__(content, classes="agent-message")
        self.border_title = "Assistant"
