"""PromptProvider -- orchestrates prompt generation by gathering context.

# Ref: gemini-cli PromptProvider
# (packages/core/src/prompts/promptProvider.ts)
"""

import re
from pathlib import Path

from code_agent.prompts.user_context_loader import load_user_context
from code_agent.prompts.system_prompt import get_core_system_prompt, compose_system_prompt


class PromptProvider:
    """Orchestrates prompt generation by gathering context and options.

    # Ref: gemini-cli PromptProvider
    # (packages/core/src/prompts/promptProvider.ts)
    """

    def get_system_instruction(
        self,
        project_dir: Path | None = None,
    ) -> str:
        """Generate the core system instruction.

        # Ref: gemini-cli PromptProvider.getCoreSystemPrompt

        Args:
            project_dir: Project root directory. Defaults to cwd.
        """
        effective_project_dir = project_dir or Path.cwd()
        base_prompt = get_core_system_prompt()
        user_context = load_user_context(project_dir=effective_project_dir)
        final_prompt = compose_system_prompt(base_prompt, user_context)
        sanitized = re.sub(r"\n{3,}", "\n\n", final_prompt)

        return sanitized
