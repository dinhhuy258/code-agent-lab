from collections.abc import Generator

from code_agent.core.agent_client import AgentClient
from code_agent.core.events import (
    AgentEvent,
    TextChunk,
    TextResponse,
    ToolCallEnd,
    ToolCallStart,
    ToolCallUpdate,
)
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
        self, request: GenerateContentRequest
    ) -> Generator[TurnResult, None, None]:
        result = next(self._results)
        # Simulate streaming: yield text in chunks, then the final result
        if result.text and not result.function_calls:
            for char in result.text:
                yield TurnResult(text=char)
        yield result


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
        return ToolDeclaration(
            name="write_file", description="Write file", parameters={}
        )

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(content="File written.")

    def needs_confirmation(self, **kwargs) -> bool:
        return True


class FailingTool(BaseTool):
    def get_name(self) -> str:
        return "fail_tool"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(name="fail_tool", description="Fails", parameters={})

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(content="", error="Something went wrong")


def _make_registry(*tools: BaseTool) -> ToolRegistry:
    registry = ToolRegistry()
    for tool in tools:
        registry.register(tool)
    return registry


def _always_approve(fc: FunctionCall) -> bool:
    return True


def _always_deny(fc: FunctionCall) -> bool:
    return False


def _collect_events(agent: AgentClient, message: str) -> list[AgentEvent]:
    return list(agent.send(message))


class TestAgentClientNoTools:
    def test_simple_text_response(self) -> None:
        client = FakeLLMClient([TurnResult(text="Hello!")])
        agent = AgentClient(client=client, tool_registry=_make_registry())
        events = _collect_events(agent, "Hi")
        chunks = [e for e in events if isinstance(e, TextChunk)]
        texts = [e for e in events if isinstance(e, TextResponse)]
        # Streaming yields text chunks followed by a final TextResponse
        assert len(chunks) > 0
        assert len(texts) == 1
        assert texts[0].text == "Hello!"

    def test_preserves_conversation(self) -> None:
        client = FakeLLMClient([TurnResult(text="R1"), TurnResult(text="R2")])
        agent = AgentClient(client=client, tool_registry=_make_registry())
        _collect_events(agent, "M1")
        events = _collect_events(agent, "M2")
        texts = [e for e in events if isinstance(e, TextResponse)]
        assert texts[-1].text == "R2"

    def test_system_instruction_forwarded(self) -> None:
        requests: list[GenerateContentRequest] = []

        class CapturingClient:
            def generate_content(self, request: GenerateContentRequest) -> TurnResult:
                requests.append(request)
                return TurnResult(text="ok")

            def generate_content_stream(
                self, request: GenerateContentRequest
            ) -> Generator[TurnResult, None, None]:
                requests.append(request)
                yield TurnResult(text="ok")

        agent = AgentClient(
            client=CapturingClient(),
            tool_registry=_make_registry(),
            system_instruction="Be concise.",
        )
        _collect_events(agent, "Hi")
        assert requests[0].system_instruction == "Be concise."


class TestAgentClientToolLoop:
    def test_single_tool_call_yields_events(self) -> None:
        fc = FunctionCall(name="glob", args={"pattern": "*.py"}, call_id="c1")
        client = FakeLLMClient(
            [
                TurnResult(text="", function_calls=[fc]),
                TurnResult(text="Found files."),
            ]
        )
        agent = AgentClient(client=client, tool_registry=_make_registry(FakeGlobTool()))
        events = _collect_events(agent, "Find files")

        starts = [e for e in events if isinstance(e, ToolCallStart)]
        ends = [e for e in events if isinstance(e, ToolCallEnd)]
        texts = [e for e in events if isinstance(e, TextResponse)]
        assert len(starts) == 1
        assert starts[0].name == "glob"
        assert starts[0].call_id == "c1"
        assert starts[0].args == {"pattern": "*.py"}
        assert len(ends) == 1
        assert ends[0].name == "glob"
        assert ends[0].call_id == "c1"
        assert ends[0].error is None
        assert len(texts) == 1
        assert texts[0].text == "Found files."

    def test_multi_step_tool_calls(self) -> None:
        fc1 = FunctionCall(name="glob", args={"pattern": "*.py"}, call_id="c1")
        fc2 = FunctionCall(name="glob", args={"pattern": "*.md"}, call_id="c2")
        client = FakeLLMClient(
            [
                TurnResult(text="", function_calls=[fc1]),
                TurnResult(text="", function_calls=[fc2]),
                TurnResult(text="Done."),
            ]
        )
        agent = AgentClient(client=client, tool_registry=_make_registry(FakeGlobTool()))
        events = _collect_events(agent, "Find all files")

        starts = [e for e in events if isinstance(e, ToolCallStart)]
        ends = [e for e in events if isinstance(e, ToolCallEnd)]
        texts = [e for e in events if isinstance(e, TextResponse)]
        assert len(starts) == 2
        assert len(ends) == 2
        assert len(texts) == 1
        assert texts[0].text == "Done."

    def test_tool_needing_confirmation_approved(self) -> None:
        fc = FunctionCall(
            name="write_file", args={"file_path": "x.py", "content": "hi"}, call_id="c1"
        )
        client = FakeLLMClient(
            [
                TurnResult(text="", function_calls=[fc]),
                TurnResult(text="File written."),
            ]
        )
        agent = AgentClient(
            client=client,
            tool_registry=_make_registry(FakeWriteTool()),
            confirm_callback=_always_approve,
        )
        events = _collect_events(agent, "Write a file")

        ends = [e for e in events if isinstance(e, ToolCallEnd)]
        assert len(ends) == 1
        assert ends[0].error is None

    def test_tool_needing_confirmation_denied(self) -> None:
        fc = FunctionCall(
            name="write_file", args={"file_path": "x.py", "content": "hi"}, call_id="c1"
        )
        client = FakeLLMClient(
            [
                TurnResult(text="", function_calls=[fc]),
                TurnResult(text="OK, won't write."),
            ]
        )
        agent = AgentClient(
            client=client,
            tool_registry=_make_registry(FakeWriteTool()),
            confirm_callback=_always_deny,
        )
        events = _collect_events(agent, "Write a file")

        ends = [e for e in events if isinstance(e, ToolCallEnd)]
        assert len(ends) == 1
        assert ends[0].error is not None
        assert "denied" in ends[0].error.lower()

    def test_unknown_tool_yields_error_end(self) -> None:
        fc = FunctionCall(name="nonexistent", args={}, call_id="c1")
        client = FakeLLMClient(
            [
                TurnResult(text="", function_calls=[fc]),
                TurnResult(text="Sorry."),
            ]
        )
        agent = AgentClient(client=client, tool_registry=_make_registry())
        events = _collect_events(agent, "Do something")

        ends = [e for e in events if isinstance(e, ToolCallEnd)]
        assert len(ends) == 1
        assert ends[0].error is not None
        assert "Unknown tool" in ends[0].error

    def test_tool_execution_error(self) -> None:
        fc = FunctionCall(name="fail_tool", args={}, call_id="c1")
        client = FakeLLMClient(
            [
                TurnResult(text="", function_calls=[fc]),
                TurnResult(text="Tool failed."),
            ]
        )
        agent = AgentClient(client=client, tool_registry=_make_registry(FailingTool()))
        events = _collect_events(agent, "Do something")

        ends = [e for e in events if isinstance(e, ToolCallEnd)]
        assert len(ends) == 1
        assert ends[0].error is not None
        assert "Something went wrong" in ends[0].error

    def test_max_turns_exceeded(self) -> None:
        fc = FunctionCall(name="glob", args={"pattern": "*.py"}, call_id="c1")
        results = [TurnResult(text="", function_calls=[fc])] * 30
        client = FakeLLMClient(results)
        agent = AgentClient(client=client, tool_registry=_make_registry(FakeGlobTool()))
        events = _collect_events(agent, "Loop forever")

        texts = [e for e in events if isinstance(e, TextResponse)]
        assert len(texts) == 1
        assert "Max turns" in texts[0].text

    def test_no_confirmation_callback_auto_approves(self) -> None:
        fc = FunctionCall(
            name="write_file", args={"file_path": "x.py", "content": "hi"}, call_id="c1"
        )
        client = FakeLLMClient(
            [
                TurnResult(text="", function_calls=[fc]),
                TurnResult(text="Written."),
            ]
        )
        agent = AgentClient(
            client=client,
            tool_registry=_make_registry(FakeWriteTool()),
        )
        events = _collect_events(agent, "Write a file")

        ends = [e for e in events if isinstance(e, ToolCallEnd)]
        assert len(ends) == 1
        assert ends[0].error is None


class TestAgentClientToolCallUpdate:
    def test_task_tool_yields_updates(self) -> None:
        class FakeTaskTool(BaseTool):
            def get_name(self) -> str:
                return "task"

            def get_declaration(self) -> ToolDeclaration:
                return ToolDeclaration(name="task", description="Task", parameters={})

            def execute(self, **kwargs) -> ToolResult:
                on_output = kwargs.get("on_output")
                if on_output:
                    on_output(
                        [
                            {
                                "type": "tool_start",
                                "name": "grep_search",
                                "status": "running",
                            }
                        ]
                    )
                    on_output(
                        [
                            {
                                "type": "tool_end",
                                "name": "grep_search",
                                "status": "completed",
                            }
                        ]
                    )
                return ToolResult(content="Task done.")

        fc = FunctionCall(name="task", args={"prompt": "find auth"}, call_id="c1")
        client = FakeLLMClient(
            [
                TurnResult(text="", function_calls=[fc]),
                TurnResult(text="Found it."),
            ]
        )
        agent = AgentClient(client=client, tool_registry=_make_registry(FakeTaskTool()))
        events = _collect_events(agent, "Find auth")

        updates = [e for e in events if isinstance(e, ToolCallUpdate)]
        assert len(updates) == 2
        assert updates[0].call_id == "c1"

    def test_normal_tool_no_updates(self) -> None:
        fc = FunctionCall(name="glob", args={"pattern": "*.py"}, call_id="c1")
        client = FakeLLMClient(
            [
                TurnResult(text="", function_calls=[fc]),
                TurnResult(text="Found files."),
            ]
        )
        agent = AgentClient(client=client, tool_registry=_make_registry(FakeGlobTool()))
        events = _collect_events(agent, "Find files")

        updates = [e for e in events if isinstance(e, ToolCallUpdate)]
        assert len(updates) == 0
