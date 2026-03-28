from collections.abc import Generator

from code_agent.llm.types import GenerateContentRequest, TurnResult
from code_agent.tools.default_registry import create_default_registry

class FakeLLMClient:
    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        return TurnResult(text="ok")

    def generate_content_stream(
        self, request: GenerateContentRequest,
    ) -> Generator[TurnResult, None, None]:
        yield TurnResult(text="ok")

class TestDefaultRegistry:
    def test_all_tools_registered_without_llm(self) -> None:
        registry = create_default_registry()
        expected_tools = [
            "glob",
            "read_file",
            "write_file",
            "replace",
            "list_directory",
            "grep_search",
            "web_fetch",
            "run_shell_command",
        ]
        for name in expected_tools:
            assert registry.get_tool(name) is not None, f"Tool '{name}' not registered"
        assert registry.get_tool("task") is None

    def test_declarations_count_without_llm(self) -> None:
        registry = create_default_registry()
        declarations = registry.get_declarations()
        assert len(declarations) == 8

    def test_task_tool_registered_with_llm(self) -> None:
        registry = create_default_registry(llm_client=FakeLLMClient())
        assert registry.get_tool("task") is not None

    def test_declarations_count_with_llm(self) -> None:
        registry = create_default_registry(llm_client=FakeLLMClient())
        declarations = registry.get_declarations()
        assert len(declarations) == 9
