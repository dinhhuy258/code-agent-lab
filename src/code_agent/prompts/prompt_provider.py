"""PromptProvider -- orchestrates prompt generation."""

import re

from code_agent.prompts.system_prompt import get_core_system_prompt


class PromptProvider:
    """Orchestrates prompt generation."""

    def get_system_instruction(self) -> str:
        """Generate the core system instruction."""
        prompt = get_core_system_prompt()
        return re.sub(r"\n{3,}", "\n\n", prompt)
