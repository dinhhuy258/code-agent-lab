import pytest

from code_agent.core.chat_session import ChatSession
from code_agent.llm.types import (
    GenerateContentRequest,
    LLMError,
    TurnResult,
)


class FakeLLMClient:
    def __init__(self, responses: list[str]) -> None:
        self._responses = iter(responses)

    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        return TurnResult(text=next(self._responses))


class FailingLLMClient:
    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        raise LLMError("Network error")


class TestChatSession:
    def test_send_message_returns_response_text(self) -> None:
        client = FakeLLMClient(["Hello!"])
        session = ChatSession(client=client)
        response = session.send_message("Hi")
        assert response == "Hello!"

    def test_history_grows_after_send(self) -> None:
        client = FakeLLMClient(["R1", "R2"])
        session = ChatSession(client=client)
        session.send_message("M1")
        session.send_message("M2")
        history = session.get_history()
        assert len(history) == 4  # 2 user + 2 model
        assert history[0].role == "user"
        assert history[0].parts[0].text == "M1"
        assert history[1].role == "model"
        assert history[1].parts[0].text == "R1"
        assert history[2].role == "user"
        assert history[2].parts[0].text == "M2"
        assert history[3].role == "model"
        assert history[3].parts[0].text == "R2"

    def test_system_instruction_passed_in_request(self) -> None:
        requests: list[GenerateContentRequest] = []

        class CapturingClient:
            def generate_content(self, request: GenerateContentRequest) -> TurnResult:
                requests.append(request)
                return TurnResult(text="ok")

        session = ChatSession(
            client=CapturingClient(),
            system_instruction="You are helpful.",
        )
        session.send_message("Hi")
        assert requests[0].system_instruction == "You are helpful."

    def test_llm_error_returns_error_string(self) -> None:
        client = FailingLLMClient()
        session = ChatSession(client=client)
        response = session.send_message("Hi")
        assert "Network error" in response

    def test_failed_response_not_in_history(self) -> None:
        client = FailingLLMClient()
        session = ChatSession(client=client)
        session.send_message("Hi")
        history = session.get_history()
        # User message is kept, but no model response
        assert len(history) == 1
        assert history[0].role == "user"
