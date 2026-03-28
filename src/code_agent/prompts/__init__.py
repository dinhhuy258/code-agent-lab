"""Prompt management system for the code agent.

# Public API mirrors gemini-cli core/prompts.ts
"""

from pathlib import Path

from code_agent.prompts.prompt_provider import PromptProvider
from code_agent.prompts.system_prompt import UserContext

def get_system_instruction(
    project_dir: Path = Path.cwd(),
) -> str:
    """Return the core system instruction for the agent.

    """
    return PromptProvider().get_system_instruction(
        project_dir=project_dir,
    )
