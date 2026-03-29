"""Tests for PromptProvider orchestrator."""

from code_agent.prompts.prompt_provider import PromptProvider


class TestPromptProvider:
    def test_returns_non_empty_prompt(self) -> None:
        provider = PromptProvider()
        result = provider.get_system_instruction()
        assert len(result) > 0

    def test_includes_preamble(self) -> None:
        provider = PromptProvider()
        result = provider.get_system_instruction()
        assert "Code Agent" in result

    def test_no_triple_newlines(self) -> None:
        provider = PromptProvider()
        result = provider.get_system_instruction()
        assert "\n\n\n" not in result
