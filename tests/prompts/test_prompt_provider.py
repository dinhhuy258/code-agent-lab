"""Tests for PromptProvider orchestrator.

# Ref: gemini-cli promptProvider.ts
"""

from pathlib import Path

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

    def test_includes_core_mandates(self) -> None:
        provider = PromptProvider()
        result = provider.get_system_instruction()
        assert "Core Mandates" in result

    def test_includes_operational_guidelines(self) -> None:
        provider = PromptProvider()
        result = provider.get_system_instruction()
        assert "Operational Guidelines" in result

    def test_no_triple_newlines(self) -> None:
        provider = PromptProvider()
        result = provider.get_system_instruction()
        assert "\n\n\n" not in result

    def test_user_context_included(self, tmp_path: Path) -> None:
        agent_dir = tmp_path / ".agent"
        agent_dir.mkdir()
        (agent_dir / "AGENT.md").write_text("Always use ruff for linting.")

        provider = PromptProvider()
        result = provider.get_system_instruction(project_dir=tmp_path)
        assert "Always use ruff for linting." in result
