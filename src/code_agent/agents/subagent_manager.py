"""SubagentManager -- registry mapping subagent types to system prompts.

# Ref: gemini-cli agent definitions (packages/core/src/agents/types.ts)
"""

GENERAL_PURPOSE_PROMPT = """\
You are a sub-agent for Code Agent CLI.
Given the user's message, complete the task using available tools.
Do what has been asked; nothing more, nothing less.
When you complete the task, respond with a detailed writeup of your findings.

Your strengths:
- Searching for code across large codebases
- Analyzing multiple files to understand architecture
- Investigating complex questions requiring reading many files
- Running shell commands to gather information

Important rules:
- You are running in non-interactive mode. You CANNOT ask the user for input.
- Work systematically using available tools to complete your task.
- When done, respond with your final answer as plain text (no tool calls).
"""


class SubagentManager:
    """Maps subagent type strings to system prompts.

    # Ref: gemini-cli SubagentToolWrapper (packages/core/src/agents/subagent-tool-wrapper.ts)
    """

    def __init__(self) -> None:
        self._prompts: dict[str, str] = {}
        self.register("general-purpose", GENERAL_PURPOSE_PROMPT)

    def register(self, agent_type: str, prompt: str) -> None:
        """Register a system prompt for a subagent type."""
        self._prompts[agent_type] = prompt

    def get_prompt(self, agent_type: str) -> str:
        """Return the system prompt for the given type.

        Raises:
            ValueError: If the agent type is not registered.
        """
        if agent_type not in self._prompts:
            raise ValueError(f"Unknown subagent type: '{agent_type}'")
        return self._prompts[agent_type]
