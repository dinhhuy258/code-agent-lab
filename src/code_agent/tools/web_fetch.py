"""WebFetchTool -- fetch and return content from URLs."""

import html.parser
import re
import urllib.error
import urllib.request
from urllib.parse import urlparse

from code_agent.llm.types import ToolDeclaration
from code_agent.tools.base import BaseTool, ToolResult

MAX_CONTENT_LENGTH = 250_000
FETCH_TIMEOUT = 10


class _HTMLTextExtractor(html.parser.HTMLParser):
    """Simple HTML-to-text converter."""

    def __init__(self) -> None:
        super().__init__()
        self._texts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in ("script", "style"):
            self._skip = True

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self._skip = False

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self._texts.append(data)

    def get_text(self) -> str:
        return " ".join(self._texts)


class WebFetchTool(BaseTool):
    """Fetch and return content from a URL."""

    def get_name(self) -> str:
        return "web_fetch"

    def get_declaration(self) -> ToolDeclaration:
        return ToolDeclaration(
            name="web_fetch",
            description="Fetches content from a URL and returns the text content.",
            parameters={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch. Must start with http:// or https://.",
                    },
                },
                "required": ["url"],
            },
        )

    def execute(self, **kwargs) -> ToolResult:
        url: str = kwargs.get("url", "")

        if not url:
            return ToolResult(content="", error="url is required.")

        try:
            parsed = urlparse(url)
        except ValueError:
            return ToolResult(content="", error=f"Invalid URL: {url}")

        if parsed.scheme not in ("http", "https"):
            return ToolResult(
                content="", error=f"Invalid URL scheme. Must be http or https: {url}"
            )

        if not parsed.hostname:
            return ToolResult(content="", error=f"Invalid URL: {url}")

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "code-agent/0.1"})
            with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as response:
                raw = response.read(MAX_CONTENT_LENGTH)
                content_type = response.headers.get_content_type()
        except urllib.error.URLError as e:
            return ToolResult(content="", error=f"Failed to fetch URL: {e}")
        except TimeoutError:
            return ToolResult(
                content="", error=f"Request timed out after {FETCH_TIMEOUT}s."
            )

        text = raw.decode("utf-8", errors="replace")

        if content_type and "html" in content_type:
            extractor = _HTMLTextExtractor()
            extractor.feed(text)
            text = extractor.get_text()

        text = re.sub(r"\s+", " ", text).strip()

        if len(text) > MAX_CONTENT_LENGTH:
            text = text[:MAX_CONTENT_LENGTH] + "\n\n[Content truncated.]"

        return ToolResult(content=f"Content from {url}:\n\n{text}")
