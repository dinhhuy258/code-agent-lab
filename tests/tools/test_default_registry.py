from collections.abc import Generator
from pathlib import Path

from code_agent.llm.types import GenerateContentRequest, TurnResult
from code_agent.skills.skill_manager import SkillManager
from code_agent.tools.default_registry import create_default_registry


class FakeLLMClient:
    model_name = "fake-model"

    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        return TurnResult(text="ok")

    def generate_content_stream(
        self,
        request: GenerateContentRequest,
    ) -> Generator[TurnResult, None, None]:
        yield TurnResult(text="ok")


def _make_skill_manager() -> SkillManager:
    return SkillManager(workspace_dir=Path.cwd())


class TestDefaultRegistry:
    def test_all_tools_registered(self) -> None:
        registry = create_default_registry(
            llm_client=FakeLLMClient(), skill_manager=_make_skill_manager()
        )
        expected_tools = [
            "glob",
            "read_file",
            "write_file",
            "replace",
            "list_directory",
            "grep_search",
            "web_fetch",
            "run_shell_command",
            "task",
        ]
        for name in expected_tools:
            assert registry.get_tool(name) is not None, f"Tool '{name}' not registered"

    def test_declarations_count(self) -> None:
        registry = create_default_registry(
            llm_client=FakeLLMClient(), skill_manager=_make_skill_manager()
        )
        declarations = registry.get_declarations()
        assert len(declarations) == 9
