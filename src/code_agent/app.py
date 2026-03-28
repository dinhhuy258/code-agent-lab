import os
from pathlib import Path

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Input
from textual.worker import get_current_worker

from code_agent.core.agent_client import AgentClient
from code_agent.core.events import TextChunk, TextResponse, ToolCallEnd, ToolCallStart, UsageUpdate
from code_agent.llm.client import LLMClient
from code_agent.llm.gemini_client import GeminiLLMClient
from code_agent.llm.types import LLMError
from code_agent.tools.default_registry import create_default_registry
from code_agent.tools.registry import ToolRegistry
from code_agent.widgets.chat_view import ChatView
from code_agent.widgets.message import AgentMessage, UserMessage
from code_agent.widgets.thinking_indicator import ThinkingIndicator
from code_agent.widgets.status_bar import StatusBar
from code_agent.widgets.tool_call import ToolCallMessage

STYLES_PATH = Path(__file__).parent.parent.parent / "styles" / "app.tcss"

SYSTEM_INSTRUCTION = """\
You are a helpful coding assistant. You have access to tools for reading files, \
writing files, searching code, running shell commands, and fetching web content. \
Use these tools to help the user with their coding tasks. \
Always read a file before attempting to modify it.\
"""


class CodeAgentApp(App[None]):
    """TUI chat interface for the code agent."""

    CSS_PATH = STYLES_PATH

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        tool_registry: ToolRegistry | None = None,
    ) -> None:
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
                tool_registry=tool_registry or create_default_registry(),
                system_instruction=SYSTEM_INSTRUCTION,
            )

        self._tool_call_widgets: dict[str, ToolCallMessage] = {}
        self._streaming_message: AgentMessage | None = None

    def compose(self) -> ComposeResult:
        yield ChatView()
        yield StatusBar()
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
            agent_message = AgentMessage("Error: GEMINI_API_KEY is not set. Please set it and restart.")
            await chat_view.mount(agent_message)
            agent_message.scroll_visible()
            return

        indicator = ThinkingIndicator()
        await chat_view.mount(indicator)
        indicator.scroll_visible()

        self._run_llm(user_text, indicator)

    @work(thread=True)
    def _run_llm(self, user_text: str, indicator: ThinkingIndicator) -> None:
        """Run the agent loop in a background thread, posting events to the UI."""
        worker = get_current_worker()
        for event in self.agent_client.send(user_text):
            if worker.is_cancelled:
                return
            if isinstance(event, TextChunk):
                self.call_from_thread(self._on_text_chunk, event, indicator)
            elif isinstance(event, ToolCallStart):
                self.call_from_thread(self._on_tool_call_start, event, indicator)
            elif isinstance(event, ToolCallEnd):
                self.call_from_thread(self._on_tool_call_end, event)
            elif isinstance(event, UsageUpdate):
                self.call_from_thread(self._on_usage_update, event)
            elif isinstance(event, TextResponse):
                self.call_from_thread(self._on_text_response, event, indicator)

    async def _on_text_chunk(self, event: TextChunk, indicator: ThinkingIndicator) -> None:
        """Append a streaming text chunk to the agent message widget."""
        chat_view = self.query_one(ChatView)

        if self._streaming_message is None:
            # First chunk — remove thinking indicator and mount the message
            try:
                await indicator.remove()
            except Exception:
                pass
            self._streaming_message = AgentMessage()
            await chat_view.mount(self._streaming_message)

        self._streaming_message.append_chunk(event.text)
        self._streaming_message.scroll_visible()

    async def _on_tool_call_start(self, event: ToolCallStart, indicator: ThinkingIndicator) -> None:
        """Mount a ToolCallMessage widget when a tool call begins."""
        chat_view = self.query_one(ChatView)
        # Remove the thinking indicator while showing tool activity
        try:
            await indicator.remove()
        except Exception:
            pass

        # Reset streaming state when entering tool call phase
        self._streaming_message = None

        tool_widget = ToolCallMessage(name=event.name, args=event.args)
        self._tool_call_widgets[event.call_id] = tool_widget
        await chat_view.mount(tool_widget)
        tool_widget.scroll_visible()

    async def _on_usage_update(self, event: UsageUpdate) -> None:
        """Update the token status bar with usage from this turn."""
        self.query_one(StatusBar).add_usage(
            prompt_tokens=event.prompt_token_count,
            candidates_tokens=event.candidates_token_count,
            total_tokens=event.total_token_count,
            cached_tokens=event.cached_content_token_count,
            thoughts_tokens=event.thoughts_token_count,
        )

    async def _on_tool_call_end(self, event: ToolCallEnd) -> None:
        """Update the ToolCallMessage widget when a tool call completes."""
        tool_widget = self._tool_call_widgets.pop(event.call_id, None)
        if tool_widget is not None:
            tool_widget.mark_complete(error=event.error)

    async def _on_text_response(self, event: TextResponse, indicator: ThinkingIndicator) -> None:
        """Show the final agent response."""
        chat_view = self.query_one(ChatView)
        # Remove thinking indicator if it's still mounted
        try:
            await indicator.remove()
        except Exception:
            pass

        if self._streaming_message is not None:
            # Streaming already populated the message — just reset state
            self._streaming_message = None
        else:
            # No streaming chunks arrived (e.g. error or tool-only response)
            agent_message = AgentMessage(event.text)
            await chat_view.mount(agent_message)
            agent_message.scroll_visible()

        self._tool_call_widgets.clear()


def main() -> None:
    app = CodeAgentApp()
    app.run()
