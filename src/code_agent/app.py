from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Input

from code_agent.services.agent_service import AgentService
from code_agent.widgets.chat_view import ChatView
from code_agent.widgets.message import AgentMessage, UserMessage

STYLES_PATH = Path(__file__).parent.parent.parent / "styles" / "app.tcss"


class CodeAgentApp(App[None]):
    """TUI chat interface for the code agent."""

    CSS_PATH = STYLES_PATH

    def __init__(self) -> None:
        super().__init__()
        self.agent_service = AgentService()

    def compose(self) -> ComposeResult:
        yield ChatView()
        yield Input(placeholder="Type a message...")

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_text = event.value.strip()
        if not user_text:
            event.input.clear()
            return

        event.input.clear()
        chat_view = self.query_one(ChatView)

        await chat_view.mount(UserMessage(user_text))
        response = self.agent_service.send(user_text)
        agent_message = AgentMessage(response)
        await chat_view.mount(agent_message)
        agent_message.scroll_visible()


def main() -> None:
    app = CodeAgentApp()
    app.run()
