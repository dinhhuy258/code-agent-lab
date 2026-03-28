from collections.abc import Generator

from code_agent.agents.subagent_manager import SubagentManager
from code_agent.llm.types import GenerateContentRequest, TurnResult
from code_agent.tools.registry import ToolRegistry
from code_agent.tools.task import TaskTool


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


class TestTaskTool:
    def test_get_name(self) -> None:
        manager = SubagentManager()
        client = FakeLLMClient([TurnResult(text="done")])
        tool = TaskTool(llm_client=client, tool_registry=ToolRegistry(), subagent_manager=manager)
        assert tool.get_name() == "task"

    def test_declaration_has_required_params(self) -> None:
        manager = SubagentManager()
        client = FakeLLMClient([TurnResult(text="done")])
        tool = TaskTool(llm_client=client, tool_registry=ToolRegistry(), subagent_manager=manager)
        decl = tool.get_declaration()
        assert decl.name == "task"
        props = decl.parameters["properties"]
        assert "description" in props
        assert "prompt" in props
        assert "subagent_type" in props
        assert "description" in decl.parameters["required"]
        assert "prompt" in decl.parameters["required"]

    def test_happy_path_returns_result(self) -> None:
        manager = SubagentManager()
        client = FakeLLMClient([TurnResult(text="Tokens are validated in auth.py:42.")])
        tool = TaskTool(llm_client=client, tool_registry=ToolRegistry(), subagent_manager=manager)
        result = tool.execute(
            description="Search for auth",
            prompt="Find where auth tokens are validated",
            subagent_type="general-purpose",
        )
        assert result.error is None
        assert "auth.py:42" in result.content

    def test_unknown_subagent_type_returns_error(self) -> None:
        manager = SubagentManager()
        client = FakeLLMClient([TurnResult(text="done")])
        tool = TaskTool(llm_client=client, tool_registry=ToolRegistry(), subagent_manager=manager)
        result = tool.execute(
            description="Test",
            prompt="Do something",
            subagent_type="nonexistent-type",
        )
        assert result.error is not None
        assert "Unknown subagent type" in result.error

    def test_prevents_recursive_calls(self) -> None:
        manager = SubagentManager()
        client = FakeLLMClient([TurnResult(text="done")])
        tool = TaskTool(llm_client=client, tool_registry=ToolRegistry(), subagent_manager=manager)

        TaskTool._depth = 1
        try:
            result = tool.execute(
                description="Nested",
                prompt="Spawn another sub-agent",
                subagent_type="general-purpose",
            )
            assert result.error is not None
            assert "Nested sub-agents are not supported" in result.error
        finally:
            TaskTool._depth = 0

    def test_handles_llm_error(self) -> None:
        class ErrorClient:
            def generate_content(self, request):
                raise RuntimeError("API down")

            def generate_content_stream(self, request):
                raise RuntimeError("API down")

        manager = SubagentManager()
        tool = TaskTool(llm_client=ErrorClient(), tool_registry=ToolRegistry(), subagent_manager=manager)
        result = tool.execute(
            description="Test error",
            prompt="Do something",
            subagent_type="general-purpose",
        )
        assert result.error is not None
        assert "Sub-agent failed" in result.error
