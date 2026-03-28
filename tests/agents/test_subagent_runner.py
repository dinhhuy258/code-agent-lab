from collections.abc import Generator

from code_agent.agents.subagent_runner import SubagentRunner
from code_agent.core.chat_session import ChatSession
from code_agent.llm.types import (
    FunctionCall,
    GenerateContentRequest,
    ToolDeclaration,
    TurnResult,
)
from code_agent.tools.base import BaseTool, ToolResult
from code_agent.tools.registry import ToolRegistry


class FakeLLMClient:
    """Returns pre-programmed TurnResults in sequence."""

    def __init__(self, results: list[TurnResult]) -> None:
        self._results = iter(results)

    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        return next(self._results)

    def generate_content_stream(
        self, request: GenerateContentRequest,
    ) -> Generator[TurnResult, None, None]:
        result = next(self._results)
        yield result


class FakeSearchTool(BaseTool):
    def get_name(self) -> str:
        return "search"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(name="search", description="Search", parameters={})

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(content="Found: auth.py:42")


class FakeFailingTool(BaseTool):
    def get_name(self) -> str:
        return "fail_tool"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(name="fail_tool", description="Fails", parameters={})

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(content="", error="Tool broke")


def _make_runner(
    results: list[TurnResult],
    tools: list[BaseTool] | None = None,
    max_turns: int = 15,
) -> SubagentRunner:
    client = FakeLLMClient(results)
    registry = ToolRegistry()
    for tool in tools or []:
        registry.register(tool)
    session = ChatSession(
        client=client,
        system_instruction="You are a test sub-agent.",
        tool_declarations=registry.get_declarations(),
    )
    return SubagentRunner(chat_session=session, tool_registry=registry, max_turns=max_turns)


class TestSubagentRunner:
    def test_returns_text_on_no_tool_calls(self) -> None:
        runner = _make_runner([TurnResult(text="The answer is 42.")])
        result = runner.run("What is the answer?")
        assert result == "The answer is 42."

    def test_executes_tools_and_continues(self) -> None:
        fc = FunctionCall(name="search", args={"query": "auth"}, call_id="c1")
        runner = _make_runner(
            [
                TurnResult(text="", function_calls=[fc]),
                TurnResult(text="Auth is in auth.py:42."),
            ],
            tools=[FakeSearchTool()],
        )
        result = runner.run("Find auth")
        assert "Auth" in result

    def test_respects_max_turns(self) -> None:
        fc = FunctionCall(name="search", args={}, call_id="c1")
        results = [TurnResult(text="still searching", function_calls=[fc])] * 5
        runner = _make_runner(results, tools=[FakeSearchTool()], max_turns=3)
        result = runner.run("Search forever")
        assert "turn limit" in result.lower()

    def test_handles_tool_error(self) -> None:
        fc = FunctionCall(name="fail_tool", args={}, call_id="c1")
        runner = _make_runner(
            [
                TurnResult(text="", function_calls=[fc]),
                TurnResult(text="Tool failed, here is my best answer."),
            ],
            tools=[FakeFailingTool()],
        )
        result = runner.run("Do something")
        assert "best answer" in result.lower()
