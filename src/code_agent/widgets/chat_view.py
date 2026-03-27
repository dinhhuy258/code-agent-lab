from textual.containers import VerticalScroll


class ChatView(VerticalScroll):
    """Scrollable container for chat messages."""

    DEFAULT_CSS = """
    ChatView {
        height: 1fr;
        padding: 1 0;
    }
    """
