from textual.widgets import Markdown, Static


class UserMessage(Static):
    """Displays a user message in the chat view."""

    DEFAULT_CSS = """
    UserMessage {
        margin: 1 0 0 2;
        padding: 1 2;
        background: $primary-background;
    }
    """

    def __init__(self, content: str) -> None:
        super().__init__(f"> {content}", classes="user-message")


class AgentMessage(Markdown):
    """Displays an agent response with markdown rendering."""

    DEFAULT_CSS = """
    AgentMessage {
        margin: 1 2 0 0;
        padding: 1 2;
        background: $surface;
    }
    """

    def __init__(self, content: str = "") -> None:
        super().__init__(content, classes="agent-message")
