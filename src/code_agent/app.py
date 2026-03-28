import os
from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Input

from code_agent.core.agent_client import AgentClient
from code_agent.llm.client import LLMClient
from code_agent.llm.gemini_client import GeminiLLMClient
from code_agent.llm.types import LLMError
from code_agent.widgets.chat_view import ChatView
from code_agent.widgets.message import AgentMessage, UserMessage

STYLES_PATH = Path(__file__).parent.parent.parent / "styles" / "app.tcss"


class CodeAgentApp(App[None]):
    """TUI chat interface for the code agent."""

    CSS_PATH = STYLES_PATH

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        super().__init__()
        if llm_client is not None:
            self._llm_client = llm_client
        else:
            try:
                api_key = os.environ.get("GEMINI_API_KEY", "")
                self._llm_client = GeminiLLMClient(api_key=api_key)
            except LLMError:
                self._llm_client = None
        self.agent_client: AgentClient | None = None
        if self._llm_client is not None:
            self.agent_client = AgentClient(
                client=self._llm_client,
                system_instruction="You are a helpful coding assistant.",
            )

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

        if self.agent_client is None:
            response = "Error: GEMINI_API_KEY is not set. Please set it and restart."
        else:
            response = self.agent_client.send(user_text)

        agent_message = AgentMessage(response)
        await chat_view.mount(agent_message)
        agent_message.scroll_visible()


def main() -> None:
    app = CodeAgentApp()
    app.run()
