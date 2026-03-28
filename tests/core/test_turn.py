import pytest

from code_agent.core.turn import Turn
from code_agent.llm.types import (
    Content,
    GenerateContentRequest,
    LLMError,
    Part,
    TurnResult,
)


class FakeLLMClient:
    def __init__(self, response: TurnResult) -> None:
        self._response = response
        self.last_request: GenerateContentRequest | None = None

    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        self.last_request = request
        return self._response


class FailingLLMClient:
    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        raise LLMError("API down")


class TestTurn:
    def test_run_returns_turn_result(self) -> None:
        client = FakeLLMClient(TurnResult(text="hello", finish_reason="STOP"))
        request = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="hi")])],
        )
        turn = Turn()
        result = turn.run(client, request)
        assert result.text == "hello"
        assert result.finish_reason == "STOP"

    def test_run_passes_request_to_client(self) -> None:
        client = FakeLLMClient(TurnResult(text="ok"))
        request = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="test")])],
            system_instruction="Be helpful.",
        )
        turn = Turn()
        turn.run(client, request)
        assert client.last_request is request

    def test_run_propagates_llm_error(self) -> None:
        client = FailingLLMClient()
        request = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="hi")])],
        )
        turn = Turn()
        with pytest.raises(LLMError, match="API down"):
            turn.run(client, request)
