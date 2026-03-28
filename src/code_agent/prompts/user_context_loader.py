"""User context loader — loads AGENT.md files from global and project directories.

# Loads user context from two tiers:
# - Global: ~/.agent/AGENT.md
# - Project: <project_dir>/.agent/AGENT.md
"""

import logging
from pathlib import Path

from code_agent.prompts.system_prompt import DEFAULT_CONTEXT_FILENAME, UserContext

logger = logging.getLogger(__name__)

DEFAULT_GLOBAL_AGENT_DIR = Path.home() / ".agent"

def load_user_context(
    project_dir: Path,
    global_agent_dir: Path = DEFAULT_GLOBAL_AGENT_DIR,
) -> UserContext:
    """Load AGENT.md files from global and project directories.

    Args:
        project_dir: The project root directory to search for
            .agent/AGENT.md.
        global_agent_dir: Override for the global agent config directory.
            Defaults to ~/.agent/.
    """

    global_content = _read_agent_md(global_agent_dir / DEFAULT_CONTEXT_FILENAME)
    project_content = _read_agent_md(project_dir / ".agent" / DEFAULT_CONTEXT_FILENAME)

    return UserContext(
        global_context=global_content,
        project_context=project_content,
    )

def _read_agent_md(file_path: Path) -> str | None:
    """Read a single AGENT.md file.

    """
    if not file_path.is_file():
        return None
    try:
        content = file_path.read_text(encoding="utf-8").strip()
        return content if content else None
    except OSError:
        logger.warning("Failed to read context file: %s", file_path)
        return None
