from code_agent.llm.types import GenerateContentRequest, TurnResult


class FakeLLMClient:
    """Fake LLM client for testing -- returns canned responses."""

    def __init__(self, responses: list[str] | None = None) -> None:
        self._responses = iter(responses or ["Mock response."])

    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        return TurnResult(text=next(self._responses))
