"""Tests for the public prompt API."""

from code_agent.prompts import get_system_instruction


class TestGetSystemInstruction:
    def test_returns_non_empty_string(self) -> None:
        result = get_system_instruction()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_includes_preamble(self) -> None:
        result = get_system_instruction()
        assert "Code Agent" in result
