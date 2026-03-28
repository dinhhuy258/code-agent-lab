from code_agent.core.chat_session import ChatSession
from code_agent.llm.types import (
    Content,
    FunctionCall,
    FunctionResponse,
    GenerateContentRequest,
    LLMError,
    Part,
    ToolDeclaration,
    TurnResult,
)

class FakeLLMClient:
    def __init__(self, results: list[TurnResult]) -> None:
        self._results = iter(results)

    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        return next(self._results)

class FailingLLMClient:
    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        raise LLMError("Network error")

class TestChatSession:
    def test_send_message_returns_turn_result(self) -> None:
        client = FakeLLMClient([TurnResult(text="Hello!")])
        session = ChatSession(client=client)
        session.append_user_message("Hi")
        result = session.send_message()
        assert result.text == "Hello!"
        assert result.function_calls == []

    def test_send_message_with_function_calls(self) -> None:
        fc = FunctionCall(name="glob", args={"pattern": "*.py"}, call_id="c1")
        client = FakeLLMClient([TurnResult(text="", function_calls=[fc])])
        session = ChatSession(client=client)
        session.append_user_message("Find files")
        result = session.send_message()
        assert len(result.function_calls) == 1
        assert result.function_calls[0].name == "glob"

    def test_append_user_message(self) -> None:
        client = FakeLLMClient([TurnResult(text="ok")])
        session = ChatSession(client=client)
        session.append_user_message("Hello")
        history = session.get_history()
        assert len(history) == 1
        assert history[0].role == "user"
        assert history[0].parts[0].text == "Hello"

    def test_send_message_appends_model_response_to_history(self) -> None:
        client = FakeLLMClient([TurnResult(text="Hi there!")])
        session = ChatSession(client=client)
        session.append_user_message("Hello")
        session.send_message()
        history = session.get_history()
        assert len(history) == 2
        assert history[1].role == "model"
        assert history[1].parts[0].text == "Hi there!"

    def test_send_message_appends_function_call_to_history(self) -> None:
        fc = FunctionCall(name="glob", args={"pattern": "*.py"}, call_id="c1")
        client = FakeLLMClient([TurnResult(text="", function_calls=[fc])])
        session = ChatSession(client=client)
        session.append_user_message("Find files")
        session.send_message()
        history = session.get_history()
        assert len(history) == 2
        model_content = history[1]
        assert model_content.role == "model"
        assert model_content.parts[0].function_call is not None
        assert model_content.parts[0].function_call.name == "glob"

    def test_append_function_response(self) -> None:
        client = FakeLLMClient([TurnResult(text="ok")])
        session = ChatSession(client=client)
        fc = FunctionCall(name="glob", args={"pattern": "*.py"}, call_id="c1")
        session.append_function_response(fc, {"files": ["a.py"]})
        history = session.get_history()
        assert len(history) == 1
        assert history[0].role == "user"
        assert history[0].parts[0].function_response is not None
        assert history[0].parts[0].function_response.name == "glob"

    def test_tool_declarations_passed_in_request(self) -> None:
        requests: list[GenerateContentRequest] = []

        class CapturingClient:
            def generate_content(self, request: GenerateContentRequest) -> TurnResult:
                requests.append(request)
                return TurnResult(text="ok")

        td = ToolDeclaration(name="glob", description="Find files", parameters={})
        session = ChatSession(client=CapturingClient(), tool_declarations=[td])
        session.append_user_message("Hi")
        session.send_message()
        assert len(requests[0].tools) == 1
        assert requests[0].tools[0].name == "glob"

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
        session.append_user_message("Hi")
        session.send_message()
        assert requests[0].system_instruction == "You are helpful."

    def test_llm_error_returns_error_turn_result(self) -> None:
        client = FailingLLMClient()
        session = ChatSession(client=client)
        session.append_user_message("Hi")
        result = session.send_message()
        assert "Network error" in result.text

    def test_failed_response_not_in_history(self) -> None:
        client = FailingLLMClient()
        session = ChatSession(client=client)
        session.append_user_message("Hi")
        session.send_message()
        history = session.get_history()
        assert len(history) == 1
        assert history[0].role == "user"

    def test_history_grows_across_turns(self) -> None:
        client = FakeLLMClient([TurnResult(text="R1"), TurnResult(text="R2")])
        session = ChatSession(client=client)
        session.append_user_message("M1")
        session.send_message()
        session.append_user_message("M2")
        session.send_message()
        history = session.get_history()
        assert len(history) == 4  # 2 user + 2 model
