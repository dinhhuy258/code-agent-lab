import argparse
import os
import sys
from pathlib import Path
from uuid import uuid4

from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Markdown
from textual.worker import get_current_worker

from code_agent.core.agent_client import AgentClient
from code_agent.core.events import (
    TextChunk,
    TextResponse,
    ToolCallEnd,
    ToolCallStart,
    ToolCallUpdate,
    UsageUpdate,
)
from code_agent.llm.client import LLMClient
from code_agent.llm.debug_client import DebugLLMClient
from code_agent.llm.gemini_client import GeminiLLMClient
from code_agent.llm.types import LLMError
from code_agent.prompts import get_system_instruction
from code_agent.skills.skill_manager import SkillManager
from code_agent.tools.default_registry import create_default_registry
from code_agent.tools.registry import ToolRegistry
from code_agent.widgets.chat_view import ChatView
from code_agent.widgets.message import AgentMessage, UserMessage
from code_agent.widgets.message_input import MessageInput
from code_agent.widgets.thinking_indicator import ThinkingIndicator
from code_agent.widgets.status_bar import StatusBar
from code_agent.widgets.tool_call import ToolCallMessage

STYLES_PATH = Path(__file__).parent.parent.parent / "styles" / "app.tcss"


class CodeAgentApp(App[None]):
    """TUI chat interface for the code agent."""

    CSS_PATH = STYLES_PATH

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        tool_registry: ToolRegistry | None = None,
        debug_dir: Path | None = None,
    ) -> None:
        super().__init__()
        if llm_client is not None:
            self._llm_client = llm_client
        else:
            try:
                api_key = os.environ.get("GEMINI_API_KEY", "")
                credentials_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
                self._llm_client = GeminiLLMClient(
                    api_key=api_key,
                    credentials_file=credentials_file,
                )
            except LLMError:
                self._llm_client = None

        if debug_dir is not None and self._llm_client is not None:
            self._llm_client = DebugLLMClient(self._llm_client, debug_dir)

        skill_manager = SkillManager(workspace_dir=Path.cwd())
        skill_manager.discover_skills()

        self.agent_client: AgentClient | None = None
        if self._llm_client is not None:
            _registry = tool_registry or create_default_registry(
                llm_client=self._llm_client,
                skill_manager=skill_manager,
            )
            self.agent_client = AgentClient(
                client=self._llm_client,
                tool_registry=_registry,
                system_instruction=get_system_instruction(skill_manager=skill_manager),
            )

        self._tool_call_widgets: dict[str, ToolCallMessage] = {}
        self._streaming_message: AgentMessage | None = None
        self._markdown_stream = None

    def compose(self) -> ComposeResult:
        yield ChatView()
        model_name = getattr(self._llm_client, "model_name", "")
        yield StatusBar(model_name=model_name)
        yield MessageInput()

    def on_mount(self) -> None:
        self.query_one(MessageInput).focus()

    async def on_message_input_submitted(self, event: MessageInput.Submitted) -> None:
        user_text = event.text
        chat_view = self.query_one(ChatView)

        await chat_view.mount(UserMessage(user_text))

        if self.agent_client is None:
            agent_message = AgentMessage(
                "Error: GEMINI_API_KEY is not set. Please set it and restart."
            )
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
            elif isinstance(event, ToolCallUpdate):
                self.call_from_thread(self._on_tool_call_update, event)
            elif isinstance(event, UsageUpdate):
                self.call_from_thread(self._on_usage_update, event)
            elif isinstance(event, TextResponse):
                self.call_from_thread(self._on_text_response, event, indicator)

    async def _on_text_chunk(
        self, event: TextChunk, indicator: ThinkingIndicator
    ) -> None:
        """Append a streaming text chunk to the agent message widget."""
        chat_view = self.query_one(ChatView)

        if self._streaming_message is None:
            try:
                await indicator.remove()
            except Exception:
                pass
            self._streaming_message = AgentMessage()
            await chat_view.mount(self._streaming_message)
            self._markdown_stream = Markdown.get_stream(self._streaming_message)

        await self._markdown_stream.write(event.text)
        self._streaming_message.scroll_visible()

    async def _on_tool_call_start(
        self, event: ToolCallStart, indicator: ThinkingIndicator
    ) -> None:
        """Mount a ToolCallMessage widget when a tool call begins."""
        chat_view = self.query_one(ChatView)
        try:
            await indicator.remove()
        except Exception:
            pass

        if self._markdown_stream is not None:
            await self._markdown_stream.stop()
            self._markdown_stream = None
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

    async def _on_tool_call_update(self, event: ToolCallUpdate) -> None:
        """Update the ToolCallMessage widget with sub-agent activity."""
        tool_widget = self._tool_call_widgets.get(event.call_id)
        if tool_widget is not None:
            tool_widget.update_activities(event.activities)

    async def _on_tool_call_end(self, event: ToolCallEnd) -> None:
        """Update the ToolCallMessage widget when a tool call completes."""
        tool_widget = self._tool_call_widgets.pop(event.call_id, None)
        if tool_widget is not None:
            tool_widget.mark_complete(error=event.error)

    async def _on_text_response(
        self, event: TextResponse, indicator: ThinkingIndicator
    ) -> None:
        """Show the final agent response."""
        chat_view = self.query_one(ChatView)
        try:
            await indicator.remove()
        except Exception:
            pass

        if self._streaming_message is not None:
            if self._markdown_stream is not None:
                await self._markdown_stream.stop()
                self._markdown_stream = None
            self._streaming_message = None
        else:
            agent_message = AgentMessage(event.text)
            await chat_view.mount(agent_message)
            agent_message.scroll_visible()

        self._tool_call_widgets.clear()


def main() -> None:
    parser = argparse.ArgumentParser(description="Code Agent CLI")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode: log all LLM requests/responses to .debug/<session>/",
    )
    args = parser.parse_args()

    debug_dir = None
    if args.debug:
        session_id = uuid4().hex[:8]
        debug_dir = Path.cwd() / ".debug" / session_id
        debug_dir.mkdir(parents=True, exist_ok=True)
        print(f"Debug session: {debug_dir}", file=sys.stderr)

    app = CodeAgentApp(debug_dir=debug_dir)
    app.run()
