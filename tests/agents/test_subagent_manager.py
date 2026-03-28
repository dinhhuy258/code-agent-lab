import pytest

from code_agent.agents.subagent_manager import SubagentManager


class TestSubagentManager:
    def test_register_and_get_prompt(self) -> None:
        manager = SubagentManager()
        manager.register("code-reviewer", "You are a code reviewer.")
        assert manager.get_prompt("code-reviewer") == "You are a code reviewer."

    def test_get_unknown_type_raises(self) -> None:
        manager = SubagentManager()
        with pytest.raises(ValueError, match="Unknown subagent type"):
            manager.get_prompt("nonexistent")

    def test_default_general_purpose_registered(self) -> None:
        manager = SubagentManager()
        prompt = manager.get_prompt("general-purpose")
        assert "agent" in prompt.lower()
        assert len(prompt) > 50
