import pytest

from code_agent.tools.base import BaseTool, ToolResult
from code_agent.llm.types import ToolDeclaration

class TestToolResult:
    def test_successful_result(self) -> None:
        result = ToolResult(content="file contents here")
        assert result.content == "file contents here"
        assert result.error is None

    def test_error_result(self) -> None:
        result = ToolResult(content="", error="File not found")
        assert result.error == "File not found"

class DummyTool(BaseTool):
    def get_name(self) -> str:
        return "dummy"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(
            name="dummy",
            description="A dummy tool",
            parameters={"type": "object", "properties": {}, "required": []},
        )

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(content="done")

class TestBaseTool:
    def test_get_name(self) -> None:
        tool = DummyTool()
        assert tool.get_name() == "dummy"

    def test_get_declaration(self) -> None:
        tool = DummyTool()
        decl = tool.get_declaration()
        assert decl.name == "dummy"
        assert decl.description == "A dummy tool"

    def test_execute(self) -> None:
        tool = DummyTool()
        result = tool.execute()
        assert result.content == "done"

    def test_needs_confirmation_defaults_false(self) -> None:
        tool = DummyTool()
        assert tool.needs_confirmation() is False

    def test_cannot_instantiate_abstract(self) -> None:
        with pytest.raises(TypeError):
            BaseTool()  # type: ignore[abstract]
