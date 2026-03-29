"""Prompt management system for the code agent."""

from code_agent.prompts.prompt_provider import PromptProvider


def get_system_instruction() -> str:
    """Return the core system instruction for the agent."""
    return PromptProvider().get_system_instruction()
