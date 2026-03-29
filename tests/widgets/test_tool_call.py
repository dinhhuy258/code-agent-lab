
from code_agent.core.events import SubagentActivity
from code_agent.widgets.tool_call import ToolCallMessage


class TestToolCallMessage:
    def test_initial_state_is_executing(self) -> None:
        widget = ToolCallMessage(name="read_file", args={"file_path": "app.py"})
        assert widget._tool_name == "read_file"
        assert widget._is_complete is False
        assert widget._error is None

    def test_format_args_single(self) -> None:
        widget = ToolCallMessage(name="read_file", args={"file_path": "app.py"})
        assert "file_path=app.py" in widget._format_args()

    def test_format_args_multiple(self) -> None:
        widget = ToolCallMessage(
            name="glob", args={"pattern": "*.py", "dir_path": "/src"}
        )
        formatted = widget._format_args()
        assert "pattern=*.py" in formatted
        assert "dir_path=/src" in formatted

    def test_format_args_truncates_long_values(self) -> None:
        widget = ToolCallMessage(name="write_file", args={"content": "x" * 200})
        formatted = widget._format_args()
        assert len(formatted) < 200

    def test_format_args_empty(self) -> None:
        widget = ToolCallMessage(name="glob", args={})
        assert widget._format_args() == ""

    def test_mark_complete_success(self) -> None:
        widget = ToolCallMessage(name="read_file", args={"file_path": "a.py"})
        widget.mark_complete()
        assert widget._is_complete is True
        assert widget._error is None

    def test_mark_complete_error(self) -> None:
        widget = ToolCallMessage(name="read_file", args={"file_path": "a.py"})
        widget.mark_complete(error="File not found")
        assert widget._is_complete is True
        assert widget._error == "File not found"


class TestToolCallMessageActivities:
    def test_update_activities_stores_items(self) -> None:
        widget = ToolCallMessage(name="task", args={"description": "Search"})
        activities = [
            SubagentActivity(type="tool_end", name="grep_search", status="completed"),
            SubagentActivity(type="tool_start", name="read_file", status="running"),
        ]
        widget.update_activities(activities)
        assert widget._activities == activities

    def test_update_activities_empty_list(self) -> None:
        widget = ToolCallMessage(name="task", args={"description": "Search"})
        widget.update_activities([])
        assert widget._activities == []

    def test_initial_activities_empty(self) -> None:
        widget = ToolCallMessage(name="task", args={})
        assert widget._activities == []


class TestToolCallTiming:
    def test_initial_elapsed_is_zero(self) -> None:
        widget = ToolCallMessage(name="read_file", args={"file_path": "a.py"})
        assert widget._elapsed_secs() < 0.1

    def test_format_elapsed_sub_second(self) -> None:
        widget = ToolCallMessage(name="read_file", args={"file_path": "a.py"})
        assert widget._format_elapsed(0.3) == "0.3s"

    def test_format_elapsed_seconds(self) -> None:
        widget = ToolCallMessage(name="read_file", args={"file_path": "a.py"})
        assert widget._format_elapsed(2.56) == "2.6s"

    def test_format_elapsed_minutes(self) -> None:
        widget = ToolCallMessage(name="read_file", args={"file_path": "a.py"})
        assert widget._format_elapsed(95.2) == "1m 35s"

    def test_mark_complete_freezes_timing(self) -> None:
        widget = ToolCallMessage(name="read_file", args={"file_path": "a.py"})
        widget.mark_complete()
        assert widget._end_time is not None

    def test_complete_adds_css_class_success(self) -> None:
        widget = ToolCallMessage(name="read_file", args={"file_path": "a.py"})
        widget.mark_complete()
        assert widget.has_class("success")

    def test_complete_adds_css_class_error(self) -> None:
        widget = ToolCallMessage(name="read_file", args={"file_path": "a.py"})
        widget.mark_complete(error="File not found")
        assert widget.has_class("error")
