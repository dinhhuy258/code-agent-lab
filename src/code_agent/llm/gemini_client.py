"""Gemini API implementation of LLMClient.

# Ref: gemini-cli createContentGenerator (packages/core/src/core/contentGenerator.ts)
# Wraps the google-genai Python SDK. Converts our types to/from SDK types.
"""

import uuid

from google import genai
from google.genai import types as genai_types

from code_agent.llm.types import (
    FunctionCall,
    GenerateContentRequest,
    LLMError,
    ToolDeclaration,
    TurnResult,
)


class GeminiLLMClient:
    """LLM client backed by the Google Gemini API.

    # Ref: gemini-cli ContentGenerator (packages/core/src/core/contentGenerator.ts)
    """

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash") -> None:
        if not api_key:
            raise LLMError("GEMINI_API_KEY is required but was empty.")
        self._model = model
        self._client = genai.Client(api_key=api_key)

    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        """Send a request to the Gemini API and return a TurnResult.

        # Ref: gemini-cli GeminiChat.makeApiCallAndProcessStream
        """
        sdk_contents = self._build_sdk_contents(request)
        config = self._build_sdk_config(request)

        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=sdk_contents,
                config=config,
            )
        except Exception as e:
            raise LLMError(str(e)) from e

        return self._parse_response(response)

    def _build_sdk_contents(self, request: GenerateContentRequest) -> list[genai_types.Content]:
        """Convert internal Content objects to SDK format."""
        sdk_contents = []
        for content in request.contents:
            sdk_parts = []
            for part in content.parts:
                if part.text is not None:
                    sdk_parts.append(genai_types.Part.from_text(text=part.text))
                elif part.function_call is not None:
                    sdk_parts.append(
                        genai_types.Part.from_function_call(
                            name=part.function_call.name,
                            args=part.function_call.args,
                        )
                    )
                elif part.function_response is not None:
                    sdk_parts.append(
                        genai_types.Part.from_function_response(
                            name=part.function_response.name,
                            response=part.function_response.response,
                        )
                    )
            sdk_contents.append(genai_types.Content(role=content.role, parts=sdk_parts))
        return sdk_contents

    def _build_sdk_config(self, request: GenerateContentRequest) -> genai_types.GenerateContentConfig:
        """Build the SDK config including system instruction and tools."""
        tools = None
        if request.tools:
            tools = [
                genai_types.Tool(
                    function_declarations=[
                        genai_types.FunctionDeclaration(
                            name=td.name,
                            description=td.description,
                            parameters=td.parameters,
                        )
                        for td in request.tools
                    ]
                )
            ]

        return genai_types.GenerateContentConfig(
            system_instruction=request.system_instruction,
            tools=tools,
        )

    def _parse_response(self, response) -> TurnResult:
        """Parse the SDK response into a TurnResult with function calls."""
        text = response.text or ""
        function_calls: list[FunctionCall] = []

        if response.candidates:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if part.function_call:
                        call_id = getattr(part.function_call, "id", None) or str(uuid.uuid4())
                        function_calls.append(
                            FunctionCall(
                                name=part.function_call.name,
                                args=dict(part.function_call.args) if part.function_call.args else {},
                                call_id=call_id,
                            )
                        )

        if not text and not function_calls:
            text = "No response received."

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

        return TurnResult(
            text=text,
            function_calls=function_calls,
            finish_reason=finish_reason,
            usage=usage,
        )
