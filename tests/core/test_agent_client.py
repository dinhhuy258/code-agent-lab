from collections.abc import Callable
from typing import Any

from code_agent.core.agent_client import AgentClient
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


class FakeGlobTool(BaseTool):
    def get_name(self) -> str:
        return "glob"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(name="glob", description="Find files", parameters={})

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(content="a.py\nb.py")


class FakeWriteTool(BaseTool):
    def get_name(self) -> str:
        return "write_file"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(name="write_file", description="Write file", parameters={})

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(content="File written.")

    def needs_confirmation(self, **kwargs) -> bool:
        return True


def _make_registry(*tools: BaseTool) -> ToolRegistry:
    registry = ToolRegistry()
    for tool in tools:
        registry.register(tool)
    return registry


def _always_approve(fc: FunctionCall) -> bool:
    return True


def _always_deny(fc: FunctionCall) -> bool:
    return False


class TestAgentClientNoTools:
    def test_simple_text_response(self) -> None:
        client = FakeLLMClient([TurnResult(text="Hello!")])
        agent = AgentClient(client=client, tool_registry=_make_registry())
        response = agent.send("Hi")
        assert response == "Hello!"

    def test_preserves_conversation(self) -> None:
        client = FakeLLMClient([TurnResult(text="R1"), TurnResult(text="R2")])
        agent = AgentClient(client=client, tool_registry=_make_registry())
        agent.send("M1")
        response = agent.send("M2")
        assert response == "R2"

    def test_system_instruction_forwarded(self) -> None:
        requests: list[GenerateContentRequest] = []

        class CapturingClient:
            def generate_content(self, request: GenerateContentRequest) -> TurnResult:
                requests.append(request)
                return TurnResult(text="ok")

        agent = AgentClient(
            client=CapturingClient(),
            tool_registry=_make_registry(),
            system_instruction="Be concise.",
        )
        agent.send("Hi")
        assert requests[0].system_instruction == "Be concise."


class TestAgentClientToolLoop:
    def test_single_tool_call(self) -> None:
        fc = FunctionCall(name="glob", args={"pattern": "*.py"}, call_id="c1")
        client = FakeLLMClient([
            TurnResult(text="", function_calls=[fc]),
            TurnResult(text="Found 2 Python files: a.py and b.py"),
        ])
        agent = AgentClient(
            client=client,
            tool_registry=_make_registry(FakeGlobTool()),
        )
        response = agent.send("Find Python files")
        assert "Found 2 Python files" in response

    def test_multi_step_tool_calls(self) -> None:
        fc1 = FunctionCall(name="glob", args={"pattern": "*.py"}, call_id="c1")
        fc2 = FunctionCall(name="glob", args={"pattern": "*.md"}, call_id="c2")
        client = FakeLLMClient([
            TurnResult(text="", function_calls=[fc1]),
            TurnResult(text="", function_calls=[fc2]),
            TurnResult(text="Done."),
        ])
        agent = AgentClient(
            client=client,
            tool_registry=_make_registry(FakeGlobTool()),
        )
        response = agent.send("Find all files")
        assert response == "Done."

    def test_tool_needing_confirmation_approved(self) -> None:
        fc = FunctionCall(name="write_file", args={"file_path": "x.py", "content": "hi"}, call_id="c1")
        client = FakeLLMClient([
            TurnResult(text="", function_calls=[fc]),
            TurnResult(text="File written."),
        ])
        agent = AgentClient(
            client=client,
            tool_registry=_make_registry(FakeWriteTool()),
            confirm_callback=_always_approve,
        )
        response = agent.send("Write a file")
        assert "File written" in response

    def test_tool_needing_confirmation_denied(self) -> None:
        fc = FunctionCall(name="write_file", args={"file_path": "x.py", "content": "hi"}, call_id="c1")
        client = FakeLLMClient([
            TurnResult(text="", function_calls=[fc]),
            TurnResult(text="OK, I won't write the file."),
        ])
        agent = AgentClient(
            client=client,
            tool_registry=_make_registry(FakeWriteTool()),
            confirm_callback=_always_deny,
        )
        response = agent.send("Write a file")
        assert "won't write" in response

    def test_unknown_tool_returns_error_to_model(self) -> None:
        fc = FunctionCall(name="nonexistent", args={}, call_id="c1")
        client = FakeLLMClient([
            TurnResult(text="", function_calls=[fc]),
            TurnResult(text="Sorry, that tool doesn't exist."),
        ])
        agent = AgentClient(
            client=client,
            tool_registry=_make_registry(),
        )
        response = agent.send("Do something")
        assert "doesn't exist" in response

    def test_max_turns_exceeded(self) -> None:
        fc = FunctionCall(name="glob", args={"pattern": "*.py"}, call_id="c1")
        # Create enough results to exceed MAX_TURNS
        results = [TurnResult(text="", function_calls=[fc])] * 30
        client = FakeLLMClient(results)
        agent = AgentClient(
            client=client,
            tool_registry=_make_registry(FakeGlobTool()),
        )
        response = agent.send("Loop forever")
        assert "Max turns" in response

    def test_no_confirmation_callback_auto_approves(self) -> None:
        fc = FunctionCall(name="write_file", args={"file_path": "x.py", "content": "hi"}, call_id="c1")
        client = FakeLLMClient([
            TurnResult(text="", function_calls=[fc]),
            TurnResult(text="Written."),
        ])
        agent = AgentClient(
            client=client,
            tool_registry=_make_registry(FakeWriteTool()),
        )
        response = agent.send("Write a file")
        assert "Written" in response
