import pytest

from code_agent.tools.base import BaseTool, ToolResult
from code_agent.tools.registry import ToolRegistry
from code_agent.llm.types import ToolDeclaration


class FakeTool(BaseTool):
    def __init__(self, name: str = "fake_tool") -> None:
        self._name = name

    def get_name(self) -> str:
        return self._name

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(
            name=self._name,
            description=f"A fake {self._name}",
            parameters={"type": "object", "properties": {}, "required": []},
        )

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(content=f"executed {self._name}")


class ConfirmTool(BaseTool):
    def get_name(self) -> str:
        return "confirm_tool"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(
            name="confirm_tool",
            description="Needs confirmation",
            parameters={"type": "object", "properties": {}, "required": []},
        )

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(content="confirmed action")

    def needs_confirmation(self, **kwargs) -> bool:
        return True


class TestToolRegistry:
    def test_register_and_get_tool(self) -> None:
        registry = ToolRegistry()
        tool = FakeTool()
        registry.register(tool)
        assert registry.get_tool("fake_tool") is tool

    def test_get_tool_returns_none_for_unknown(self) -> None:
        registry = ToolRegistry()
        assert registry.get_tool("nonexistent") is None

    def test_get_declarations(self) -> None:
        registry = ToolRegistry()
        registry.register(FakeTool("tool_a"))
        registry.register(FakeTool("tool_b"))
        declarations = registry.get_declarations()
        assert len(declarations) == 2
        names = {d.name for d in declarations}
        assert names == {"tool_a", "tool_b"}

    def test_execute_known_tool(self) -> None:
        registry = ToolRegistry()
        registry.register(FakeTool("my_tool"))
        result = registry.execute("my_tool")
        assert result.content == "executed my_tool"

    def test_execute_unknown_tool_returns_error(self) -> None:
        registry = ToolRegistry()
        result = registry.execute("nonexistent")
        assert result.error is not None
        assert "Unknown tool" in result.error

    def test_execute_passes_kwargs(self) -> None:
        class EchoTool(BaseTool):
            def get_name(self) -> str:
                return "echo"

            def get_declaration(self) -> ToolDeclaration:
                return ToolDeclaration(name="echo", description="Echo", parameters={})

            def execute(self, **kwargs) -> ToolResult:
                return ToolResult(content=str(kwargs))

        registry = ToolRegistry()
        registry.register(EchoTool())
        result = registry.execute("echo", message="hello")
        assert "hello" in result.content

    def test_execute_catches_exception(self) -> None:
        class FailTool(BaseTool):
            def get_name(self) -> str:
                return "fail"

            def get_declaration(self) -> ToolDeclaration:
                return ToolDeclaration(name="fail", description="Fails", parameters={})

            def execute(self, **kwargs) -> ToolResult:
                raise RuntimeError("boom")

        registry = ToolRegistry()
        registry.register(FailTool())
        result = registry.execute("fail")
        assert result.error is not None
        assert "boom" in result.error
