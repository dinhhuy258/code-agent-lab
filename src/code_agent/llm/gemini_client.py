"""Gemini API implementation of LLMClient.

# Ref: gemini-cli createContentGenerator (packages/core/src/core/contentGenerator.ts)
# Wraps the google-genai Python SDK. Converts our types to/from SDK types.
"""

from google import genai
from google.genai import types as genai_types

from code_agent.llm.types import (
    GenerateContentRequest,
    LLMError,
    TurnResult,
)


class GeminiLLMClient:
    """LLM client backed by the Google Gemini API.

    # Ref: gemini-cli ContentGenerator (packages/core/src/core/contentGenerator.ts)
    """

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash") -> None:
        if not api_key:
            raise LLMError("GEMINI_API_KEY is required but was empty.")
        self._model = model
        self._client = genai.Client(api_key=api_key)

    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        """Send a request to the Gemini API and return a TurnResult.

        # Ref: gemini-cli GeminiChat.makeApiCallAndProcessStream
        """
        sdk_contents = [
            genai_types.Content(
                role=c.role,
                parts=[genai_types.Part.from_text(text=p.text or "") for p in c.parts],
            )
            for c in request.contents
        ]

        config = genai_types.GenerateContentConfig(
            system_instruction=request.system_instruction,
        )

        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=sdk_contents,
                config=config,
            )
        except Exception as e:
            raise LLMError(str(e)) from e

        text = response.text
        if not text:
            return TurnResult(text="No response received.")

        finish_reason = None
        if response.candidates:
            finish_reason = str(response.candidates[0].finish_reason)

        usage = None
        if response.usage_metadata:
            usage = {
                "prompt_token_count": response.usage_metadata.prompt_token_count,
                "candidates_token_count": response.usage_metadata.candidates_token_count,
                "total_token_count": response.usage_metadata.total_token_count,
            }

        return TurnResult(text=text, finish_reason=finish_reason, usage=usage)
