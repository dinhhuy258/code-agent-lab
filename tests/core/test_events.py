
from code_agent.core.events import (
    AgentEvent,
    SubagentActivity,
    TextResponse,
    ToolCallEnd,
    ToolCallStart,
    ToolCallUpdate,
)


class TestToolCallStart:
    def test_fields(self) -> None:
        event = ToolCallStart(
            name="read_file", call_id="c1", args={"file_path": "a.py"}
        )
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


class TestSubagentActivity:
    def test_fields(self) -> None:
        activity = SubagentActivity(
            type="tool_start", name="grep_search", status="running"
        )
        assert activity.type == "tool_start"
        assert activity.name == "grep_search"
        assert activity.status == "running"
        assert activity.args == ""

    def test_with_args(self) -> None:
        activity = SubagentActivity(
            type="tool_start",
            name="grep_search",
            status="running",
            args="pattern=token",
        )
        assert activity.args == "pattern=token"


class TestToolCallUpdate:
    def test_fields(self) -> None:
        activities = [
            SubagentActivity(type="tool_end", name="grep_search", status="completed"),
        ]
        event = ToolCallUpdate(call_id="c1", activities=activities)
        assert event.call_id == "c1"
        assert len(event.activities) == 1
        assert event.activities[0].name == "grep_search"


class TestAgentEventUnionIncludesUpdate:
    def test_tool_call_update_is_agent_event(self) -> None:
        update: AgentEvent = ToolCallUpdate(call_id="c1", activities=[])
        assert isinstance(update, ToolCallUpdate)
