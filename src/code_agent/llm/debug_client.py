"""Debug wrapper for LLMClient that logs requests and responses to JSON files."""

import dataclasses
import json
import sys
from collections.abc import Generator
from pathlib import Path
from typing import Any

from code_agent.llm.types import GenerateContentRequest, LLMError, TurnResult


def _to_serializable(obj: Any) -> Any:
    """Convert an object to a JSON-serializable form."""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {k: _to_serializable(v) for k, v in dataclasses.asdict(obj).items()}
    if isinstance(obj, list):
        return [_to_serializable(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _to_serializable(v) for k, v in obj.items()}
    try:
        json.dumps(obj)
        return obj
    except (TypeError, ValueError):
        return str(obj)


class DebugLLMClient:
    """LLM client wrapper that logs all requests and responses as JSON files."""

    def __init__(self, client: Any, debug_dir: Path) -> None:
        self._client = client
        self._debug_dir = debug_dir
        self._counter = 1

    @property
    def model_name(self) -> str:
        """Delegate to wrapped client."""
        return self._client.model_name

    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        """Log request/response and delegate to wrapped client."""
        counter = self._counter
        self._counter += 1

        self._write_request(counter, request)

        try:
            result = self._client.generate_content(request)
        except LLMError:
            raise
        except Exception:
            raise

        self._write_response(counter, result)
        return result

    def generate_content_stream(
        self, request: GenerateContentRequest
    ) -> Generator[TurnResult, None, None]:
        """Log request/response and delegate to wrapped client for streaming."""
        counter = self._counter
        self._counter += 1

        self._write_request(counter, request)

        final_result = None

        try:
            for result in self._client.generate_content_stream(request):
                final_result = result
                yield result
        except LLMError:
            if final_result is not None:
                self._write_response(counter, final_result)
            raise

        if final_result is not None:
            self._write_response(counter, final_result)

    def _write_request(self, counter: int, request: GenerateContentRequest) -> None:
        """Serialize and write a request to a JSON file."""
        path = self._debug_dir / f"{counter:03d}_request.json"
        data = _to_serializable(request)
        self._write_json(path, data)

    def _write_response(self, counter: int, result: TurnResult) -> None:
        """Serialize and write a response to a JSON file."""
        path = self._debug_dir / f"{counter:03d}_response.json"
        data = _to_serializable(result)
        self._write_json(path, data)

    def _write_json(self, path: Path, data: Any) -> None:
        """Write JSON data to a file, logging errors to stderr."""
        try:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        except OSError as e:
            print(f"Warning: Failed to write debug file {path}: {e}", file=sys.stderr)
