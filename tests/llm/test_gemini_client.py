from unittest.mock import MagicMock, patch

import pytest

from code_agent.llm.gemini_client import GeminiLLMClient
from code_agent.llm.types import (
    Content,
    GenerateContentRequest,
    LLMError,
    Part,
)


class TestGeminiLLMClientInit:
    def test_missing_api_key_raises_error(self) -> None:
        with pytest.raises(LLMError, match="GEMINI_API_KEY"):
            GeminiLLMClient(api_key="", model="gemini-2.0-flash")


class TestGeminiLLMClientGenerateContent:
    @patch("code_agent.llm.gemini_client.genai")
    def test_successful_response(self, mock_genai: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.text = "Hello from Gemini!"
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].finish_reason = "STOP"
        mock_response.usage_metadata = MagicMock()
        mock_response.usage_metadata.prompt_token_count = 10
        mock_response.usage_metadata.candidates_token_count = 5
        mock_response.usage_metadata.total_token_count = 15

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
        mock_response = MagicMock()
        mock_response.text = "response"
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].finish_reason = "STOP"
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
