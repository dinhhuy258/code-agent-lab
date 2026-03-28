from code_agent.llm.types import (
    Content,
    GenerateContentRequest,
    LLMError,
    Part,
    TurnResult,
)


class TestPart:
    def test_text_part(self) -> None:
        part = Part(text="hello")
        assert part.text == "hello"

    def test_part_defaults_to_none(self) -> None:
        part = Part()
        assert part.text is None


class TestContent:
    def test_user_content(self) -> None:
        content = Content(role="user", parts=[Part(text="hello")])
        assert content.role == "user"
        assert len(content.parts) == 1
        assert content.parts[0].text == "hello"


class TestTurnResult:
    def test_minimal_result(self) -> None:
        result = TurnResult(text="response")
        assert result.text == "response"
        assert result.finish_reason is None
        assert result.usage is None

    def test_full_result(self) -> None:
        result = TurnResult(
            text="response",
            finish_reason="STOP",
            usage={"prompt_tokens": 10, "completion_tokens": 5},
        )
        assert result.finish_reason == "STOP"
        assert result.usage["prompt_tokens"] == 10


class TestGenerateContentRequest:
    def test_request_with_system_instruction(self) -> None:
        req = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="hi")])],
            system_instruction="You are helpful.",
        )
        assert len(req.contents) == 1
        assert req.system_instruction == "You are helpful."

    def test_request_without_system_instruction(self) -> None:
        req = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="hi")])],
        )
        assert req.system_instruction is None


class TestLLMError:
    def test_llm_error(self) -> None:
        error = LLMError("API key invalid")
        assert str(error) == "API key invalid"
        assert isinstance(error, Exception)
