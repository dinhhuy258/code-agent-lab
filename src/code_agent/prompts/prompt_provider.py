"""PromptProvider -- orchestrates prompt generation by gathering context.

"""

import re
from pathlib import Path

from code_agent.prompts.user_context_loader import load_user_context
from code_agent.prompts.system_prompt import get_core_system_prompt, compose_system_prompt

class PromptProvider:
    """Orchestrates prompt generation by gathering context and options.

    """

    def get_system_instruction(
        self,
        project_dir: Path = Path.cwd(),
    ) -> str:
        """Generate the core system instruction.

        Args:
            project_dir: Project root directory. Defaults to cwd.
        """
        base_prompt = get_core_system_prompt()
        user_context = load_user_context(project_dir=project_dir)
        final_prompt = compose_system_prompt(base_prompt, user_context)
        sanitized = re.sub(r"\n{3,}", "\n\n", final_prompt)

        return sanitized
