"""Prompt management system for the code agent."""

from code_agent.prompts.prompt_provider import PromptProvider
from code_agent.skills.skill_manager import SkillManager


def get_system_instruction(skill_manager: SkillManager) -> str:
    """Return the core system instruction for the agent."""
    return PromptProvider(skill_manager=skill_manager).get_system_instruction()
