"""PromptProvider -- orchestrates prompt generation."""

import re

from code_agent.prompts.system_prompt import (
    get_core_system_prompt,
    render_available_skills,
)
from code_agent.skills.skill_manager import SkillManager


class PromptProvider:
    """Orchestrates prompt generation."""

    def __init__(self, skill_manager: SkillManager) -> None:
        self._skill_manager = skill_manager

    def get_system_instruction(self) -> str:
        """Generate the core system instruction."""
        prompt = get_core_system_prompt()

        skills = self._skill_manager.get_skills()
        prompt += render_available_skills(skills)

        return re.sub(r"\n{3,}", "\n\n", prompt)
