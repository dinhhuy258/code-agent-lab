"""Tests for system prompt."""

from code_agent.prompts.system_prompt import get_core_system_prompt


class TestGetCoreSystemPrompt:
    def test_includes_preamble(self) -> None:
        result = get_core_system_prompt()
        assert "interactive" in result.lower()
        assert "code agent" in result.lower()

    def test_includes_security_section(self) -> None:
        result = get_core_system_prompt()
        assert "Security" in result

    def test_includes_tool_usage(self) -> None:
        result = get_core_system_prompt()
        assert "Tool Usage" in result

    def test_includes_engineering_standards(self) -> None:
        result = get_core_system_prompt()
        assert "Engineering Standards" in result

    def test_includes_tone_and_style(self) -> None:
        result = get_core_system_prompt()
        assert "Tone" in result
