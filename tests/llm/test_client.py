from code_agent.llm.client import LLMClient
from code_agent.llm.types import (
    Content,
    GenerateContentRequest,
    Part,
    TurnResult,
)

class FakeClient:
    """A fake that structurally matches LLMClient Protocol."""

    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        return TurnResult(text="fake response")

def test_fake_client_satisfies_protocol() -> None:
    client: LLMClient = FakeClient()
    request = GenerateContentRequest(
        contents=[Content(role="user", parts=[Part(text="hi")])],
    )
    result = client.generate_content(request)
    assert result.text == "fake response"
