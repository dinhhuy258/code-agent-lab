from typing import Any

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

class TestFunctionCall:
    def test_function_call(self) -> None:
        fc = FunctionCall(name="read_file", args={"file_path": "a.py"}, call_id="call_1")
        assert fc.name == "read_file"
        assert fc.args == {"file_path": "a.py"}
        assert fc.call_id == "call_1"

class TestFunctionResponse:
    def test_function_response(self) -> None:
        fr = FunctionResponse(name="read_file", call_id="call_1", response={"content": "hello"})
        assert fr.name == "read_file"
        assert fr.call_id == "call_1"
        assert fr.response == {"content": "hello"}

class TestToolDeclaration:
    def test_tool_declaration(self) -> None:
        td = ToolDeclaration(
            name="read_file",
            description="Read a file",
            parameters={"type": "object", "properties": {"file_path": {"type": "string"}}},
        )
        assert td.name == "read_file"
        assert td.description == "Read a file"
        assert "file_path" in td.parameters["properties"]

class TestPart:
    def test_text_part(self) -> None:
        part = Part(text="hello")
        assert part.text == "hello"
        assert part.function_call is None
        assert part.function_response is None

    def test_part_defaults_to_none(self) -> None:
        part = Part()
        assert part.text is None
        assert part.function_call is None
        assert part.function_response is None

    def test_function_call_part(self) -> None:
        fc = FunctionCall(name="glob", args={"pattern": "*.py"}, call_id="c1")
        part = Part(function_call=fc)
        assert part.function_call is fc
        assert part.text is None

    def test_function_response_part(self) -> None:
        fr = FunctionResponse(name="glob", call_id="c1", response={"files": ["a.py"]})
        part = Part(function_response=fr)
        assert part.function_response is fr
        assert part.text is None

class TestTurnResult:
    def test_minimal_result(self) -> None:
        result = TurnResult(text="response")
        assert result.text == "response"
        assert result.function_calls == []
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

    def test_result_with_function_calls(self) -> None:
        fc = FunctionCall(name="glob", args={"pattern": "*.py"}, call_id="c1")
        result = TurnResult(text="", function_calls=[fc])
        assert len(result.function_calls) == 1
        assert result.function_calls[0].name == "glob"

class TestGenerateContentRequest:
    def test_request_with_tools(self) -> None:
        td = ToolDeclaration(name="glob", description="Find files", parameters={"type": "object"})
        req = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="hi")])],
            system_instruction="Be helpful.",
            tools=[td],
        )
        assert len(req.tools) == 1
        assert req.tools[0].name == "glob"

    def test_request_without_tools(self) -> None:
        req = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="hi")])],
        )
        assert req.tools == []

class TestLLMError:
    def test_llm_error(self) -> None:
        error = LLMError("API key invalid")
        assert str(error) == "API key invalid"
        assert isinstance(error, Exception)
