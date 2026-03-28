from typing import Any

from code_agent.core.events import AgentEvent, TextResponse, ToolCallEnd, ToolCallStart


class TestToolCallStart:
    def test_fields(self) -> None:
        event = ToolCallStart(name="read_file", call_id="c1", args={"file_path": "a.py"})
        assert event.name == "read_file"
        assert event.call_id == "c1"
        assert event.args == {"file_path": "a.py"}


class TestToolCallEnd:
    def test_success(self) -> None:
        event = ToolCallEnd(name="read_file", call_id="c1")
        assert event.name == "read_file"
        assert event.call_id == "c1"
        assert event.error is None

    def test_error(self) -> None:
        event = ToolCallEnd(name="read_file", call_id="c1", error="File not found")
        assert event.error == "File not found"


class TestTextResponse:
    def test_fields(self) -> None:
        event = TextResponse(text="Here are the results.")
        assert event.text == "Here are the results."


class TestAgentEventUnion:
    def test_is_union_type(self) -> None:
        start: AgentEvent = ToolCallStart(name="glob", call_id="c1", args={})
        end: AgentEvent = ToolCallEnd(name="glob", call_id="c1")
        text: AgentEvent = TextResponse(text="done")
        assert isinstance(start, ToolCallStart)
        assert isinstance(end, ToolCallEnd)
        assert isinstance(text, TextResponse)
