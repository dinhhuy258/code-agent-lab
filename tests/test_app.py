from collections.abc import Generator

from code_agent.app import CodeAgentApp
from code_agent.llm.types import FunctionCall, GenerateContentRequest, TurnResult
from code_agent.tools.base import BaseTool, ToolResult
from code_agent.tools.registry import ToolRegistry
from code_agent.llm.types import ToolDeclaration
from code_agent.widgets.message import AgentMessage, UserMessage
from code_agent.widgets.message_input import MessageInput
from code_agent.widgets.tool_call import ToolCallMessage


class FakeLLMClient:
    """Fake LLM client for testing -- returns canned responses."""

    def __init__(self, results: list[TurnResult] | None = None) -> None:
        self._results = iter(results or [TurnResult(text="Mock response.")])

    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        return next(self._results)

    def generate_content_stream(self, request: GenerateContentRequest) -> Generator[TurnResult, None, None]:
        result = next(self._results)
        if result.text and not result.function_calls:
            for char in result.text:
                yield TurnResult(text=char)
        yield result


class FakeReadTool(BaseTool):
    def get_name(self) -> str:
        return "read_file"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(name="read_file", description="Read", parameters={})

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(content="file contents")


async def _type_and_submit(pilot, text: str) -> None:
    """Type text into the focused MessageInput and press ctrl+enter."""
    app = pilot.app
    widget = app.query_one(MessageInput)
    widget.focus()
    widget.text = text
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


def _make_app(results: list[TurnResult] | None = None, registry: ToolRegistry | None = None) -> CodeAgentApp:
    """Create a CodeAgentApp with a fake LLM client."""
    return CodeAgentApp(
        llm_client=FakeLLMClient(results or [TurnResult(text="Mock response.")]),
        tool_registry=registry or ToolRegistry(),
    )


async def test_send_message_creates_widgets() -> None:
    async with _make_app([TurnResult(text="Hello!")]).run_test() as pilot:
        app = pilot.app
        await _type_and_submit(pilot, "Hello agent")
        await app.workers.wait_for_complete()
        await pilot.pause()
        user_msgs = app.query(UserMessage)
        agent_msgs = app.query(AgentMessage)
        assert len(user_msgs) == 1
        assert len(agent_msgs) == 1


async def test_empty_input_ignored() -> None:
    async with _make_app().run_test() as pilot:
        app = pilot.app
        widget = app.query_one(MessageInput)
        widget.focus()
        widget.text = "   "
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        user_msgs = app.query(UserMessage)
        assert len(user_msgs) == 0


async def test_multiple_messages() -> None:
    results = [TurnResult(text="R1"), TurnResult(text="R2"), TurnResult(text="R3")]
    async with _make_app(results).run_test() as pilot:
        app = pilot.app
        for msg in ["First", "Second", "Third"]:
            await _type_and_submit(pilot, msg)
            await app.workers.wait_for_complete()
            await pilot.pause()
        user_msgs = app.query(UserMessage)
        agent_msgs = app.query(AgentMessage)
        assert len(user_msgs) == 3
        assert len(agent_msgs) == 3


async def test_no_api_key_shows_error() -> None:
    async with CodeAgentApp(llm_client=None).run_test() as pilot:
        app = pilot.app
        await _type_and_submit(pilot, "Hello")
        agent_msgs = app.query(AgentMessage)
        assert len(agent_msgs) == 1


async def test_tool_call_shows_tool_message() -> None:
    fc = FunctionCall(name="read_file", args={"file_path": "app.py"}, call_id="c1")
    results = [
        TurnResult(text="", function_calls=[fc]),
        TurnResult(text="Here is the file content."),
    ]
    registry = ToolRegistry()
    registry.register(FakeReadTool())

    async with _make_app(results, registry).run_test() as pilot:
        app = pilot.app
        await _type_and_submit(pilot, "Read app.py")
        await app.workers.wait_for_complete()
        await pilot.pause()

        tool_msgs = app.query(ToolCallMessage)
        agent_msgs = app.query(AgentMessage)
        assert len(tool_msgs) == 1
        assert len(agent_msgs) == 1
