from unittest.mock import MagicMock, patch

import pytest

from code_agent.llm.gemini_client import GeminiLLMClient
from code_agent.llm.types import (
    Content,
    GenerateContentRequest,
    LLMError,
    Part,
    ToolDeclaration,
)

class TestGeminiLLMClientInit:
    def test_missing_api_key_raises_error(self) -> None:
        with pytest.raises(LLMError, match="GEMINI_API_KEY"):
            GeminiLLMClient(api_key="", model="gemini-2.0-flash")

class TestGeminiLLMClientGenerateContent:
    @patch("code_agent.llm.gemini_client.genai")
    def test_successful_response(self, mock_genai: MagicMock) -> None:
        mock_text_part = MagicMock()
        mock_text_part.text = "Hello from Gemini!"
        mock_text_part.thought = False
        mock_text_part.function_call = None

        mock_candidate = MagicMock()
        mock_candidate.finish_reason = "STOP"
        mock_candidate.content = MagicMock()
        mock_candidate.content.parts = [mock_text_part]

        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_response.usage_metadata = MagicMock()
        mock_response.usage_metadata.prompt_token_count = 10
        mock_response.usage_metadata.candidates_token_count = 5
        mock_response.usage_metadata.total_token_count = 15
        mock_response.usage_metadata.cached_content_token_count = 0
        mock_response.usage_metadata.thoughts_token_count = 0

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.Client.return_value = mock_client

        client = GeminiLLMClient(api_key="test-key", model="gemini-2.0-flash")
        request = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="Hello")])],
        )
        result = client.generate_content(request)

        assert result.text == "Hello from Gemini!"
        assert result.finish_reason == "STOP"
        assert result.usage["total_token_count"] == 15

    @patch("code_agent.llm.gemini_client.genai")
    def test_empty_response(self, mock_genai: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.text = None
        mock_response.candidates = []
        mock_response.usage_metadata = None

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.Client.return_value = mock_client

        client = GeminiLLMClient(api_key="test-key", model="gemini-2.0-flash")
        request = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="Hello")])],
        )
        result = client.generate_content(request)

        assert result.text == "No response received."

    @patch("code_agent.llm.gemini_client.genai")
    def test_sdk_exception_raises_llm_error(self, mock_genai: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("API failure")
        mock_genai.Client.return_value = mock_client

        client = GeminiLLMClient(api_key="test-key", model="gemini-2.0-flash")
        request = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="Hello")])],
        )
        with pytest.raises(LLMError, match="API failure"):
            client.generate_content(request)

    @patch("code_agent.llm.gemini_client.genai")
    def test_system_instruction_passed_to_sdk(self, mock_genai: MagicMock) -> None:
        mock_text_part = MagicMock()
        mock_text_part.text = "response"
        mock_text_part.thought = False
        mock_text_part.function_call = None

        mock_candidate = MagicMock()
        mock_candidate.finish_reason = "STOP"
        mock_candidate.content = MagicMock()
        mock_candidate.content.parts = [mock_text_part]

        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_response.usage_metadata = None

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.Client.return_value = mock_client

        client = GeminiLLMClient(api_key="test-key", model="gemini-2.0-flash")
        request = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="Hello")])],
            system_instruction="Be helpful.",
        )
        client.generate_content(request)

        call_kwargs = mock_client.models.generate_content.call_args
        assert call_kwargs.kwargs["config"].system_instruction == "Be helpful."

class TestGeminiLLMClientToolCalling:
    @patch("code_agent.llm.gemini_client.genai")
    def test_tool_declarations_passed_to_sdk(self, mock_genai: MagicMock) -> None:
        mock_text_part = MagicMock()
        mock_text_part.text = "I'll search for files."
        mock_text_part.thought = False
        mock_text_part.function_call = None

        mock_candidate = MagicMock()
        mock_candidate.finish_reason = "STOP"
        mock_candidate.content = MagicMock()
        mock_candidate.content.parts = [mock_text_part]

        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_response.usage_metadata = None

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.Client.return_value = mock_client

        client = GeminiLLMClient(api_key="test-key", model="gemini-2.0-flash")
        td = ToolDeclaration(
            name="glob",
            description="Find files",
            parameters={
                "type": "object",
                "properties": {"pattern": {"type": "string"}},
                "required": ["pattern"],
            },
        )
        request = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="Find py files")])],
            tools=[td],
        )
        client.generate_content(request)

        call_kwargs = mock_client.models.generate_content.call_args
        config = call_kwargs.kwargs["config"]
        assert config.tools is not None
        assert len(config.tools) == 1

    @patch("code_agent.llm.gemini_client.genai")
    def test_function_call_parsed_from_response(self, mock_genai: MagicMock) -> None:
        mock_fc = MagicMock()
        mock_fc.name = "glob"
        mock_fc.args = {"pattern": "*.py"}
        mock_fc.id = "call_123"

        mock_part = MagicMock()
        mock_part.function_call = mock_fc
        mock_part.text = None

        mock_candidate = MagicMock()
        mock_candidate.finish_reason = "STOP"
        mock_candidate.content = MagicMock()
        mock_candidate.content.parts = [mock_part]

        mock_response = MagicMock()
        mock_response.text = None
        mock_response.candidates = [mock_candidate]
        mock_response.usage_metadata = None

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.Client.return_value = mock_client

        client = GeminiLLMClient(api_key="test-key", model="gemini-2.0-flash")
        request = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="Find py files")])],
        )
        result = client.generate_content(request)

        assert len(result.function_calls) == 1
        assert result.function_calls[0].name == "glob"
        assert result.function_calls[0].args == {"pattern": "*.py"}
        assert result.function_calls[0].call_id == "call_123"

    @patch("code_agent.llm.gemini_client.genai")
    def test_mixed_text_and_function_call(self, mock_genai: MagicMock) -> None:
        mock_fc = MagicMock()
        mock_fc.name = "read_file"
        mock_fc.args = {"file_path": "a.py"}
        mock_fc.id = "call_456"

        mock_text_part = MagicMock()
        mock_text_part.function_call = None
        mock_text_part.text = "Let me read that file."
        mock_text_part.thought = False

        mock_fc_part = MagicMock()
        mock_fc_part.function_call = mock_fc
        mock_fc_part.text = None
        mock_fc_part.thought = False

        mock_candidate = MagicMock()
        mock_candidate.finish_reason = "STOP"
        mock_candidate.content = MagicMock()
        mock_candidate.content.parts = [mock_text_part, mock_fc_part]

        mock_response = MagicMock()
        mock_response.text = "Let me read that file."
        mock_response.candidates = [mock_candidate]
        mock_response.usage_metadata = None

        mock_client = MagicMock()
        mock_client.models.generate_content.return_value = mock_response
        mock_genai.Client.return_value = mock_client

        client = GeminiLLMClient(api_key="test-key", model="gemini-2.0-flash")
        request = GenerateContentRequest(
            contents=[Content(role="user", parts=[Part(text="Read a.py")])],
        )
        result = client.generate_content(request)

        assert result.text == "Let me read that file."
        assert len(result.function_calls) == 1
        assert result.function_calls[0].name == "read_file"
