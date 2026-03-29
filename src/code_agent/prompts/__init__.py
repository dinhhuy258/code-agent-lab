"""Prompt management system for the code agent."""

from code_agent.prompts.prompt_provider import PromptProvider


def get_system_instruction(skill_manager=None) -> str:
    """Return the core system instruction for the agent."""
    return PromptProvider(skill_manager=skill_manager).get_system_instruction()
