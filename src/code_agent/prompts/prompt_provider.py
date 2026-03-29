"""PromptProvider -- orchestrates prompt generation."""

import re

from code_agent.prompts.system_prompt import (
    get_core_system_prompt,
    render_available_skills,
)


class PromptProvider:
    """Orchestrates prompt generation."""

    def __init__(self, skill_manager=None) -> None:
        self._skill_manager = skill_manager

    def get_system_instruction(self) -> str:
        """Generate the core system instruction."""
        prompt = get_core_system_prompt()

        if self._skill_manager is not None:
            skills = self._skill_manager.get_skills()
            prompt += render_available_skills(skills)

        return re.sub(r"\n{3,}", "\n\n", prompt)
