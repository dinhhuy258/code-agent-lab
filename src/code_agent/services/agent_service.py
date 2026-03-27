class AgentService:
    """Handles message processing and conversation history.

    Mock implementation that echoes user input.
    Replace with real LLM client later.
    """

    def __init__(self) -> None:
        self._history: list[dict[str, str]] = []

    def send(self, user_message: str) -> str:
        """Process a user message and return an agent response."""
        self._history.append({"role": "user", "content": user_message})
        response = f'You said: "{user_message}". This is a mock response — agent integration coming soon.'
        self._history.append({"role": "agent", "content": response})
        return response

    def get_history(self) -> list[dict[str, str]]:
        """Return the full conversation history."""
        return list(self._history)
