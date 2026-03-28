from unittest.mock import MagicMock, patch

from code_agent.tools.web_fetch import WebFetchTool

class TestWebFetchTool:
    def test_get_name(self) -> None:
        assert WebFetchTool().get_name() == "web_fetch"

    def test_needs_confirmation(self) -> None:
        assert WebFetchTool().needs_confirmation() is False

    def test_get_declaration(self) -> None:
        decl = WebFetchTool().get_declaration()
        assert "url" in decl.parameters["properties"]

    @patch("code_agent.tools.web_fetch.urllib.request.urlopen")
    def test_fetch_url(self, mock_urlopen: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.read.return_value = b"<html><body>Hello World</body></html>"
        mock_response.headers.get_content_type.return_value = "text/html"
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response

        tool = WebFetchTool()
        result = tool.execute(url="https://example.com")
        assert result.error is None
        assert "Hello World" in result.content

    def test_invalid_url(self) -> None:
        tool = WebFetchTool()
        result = tool.execute(url="not-a-url")
        assert result.error is not None

    def test_missing_url(self) -> None:
        tool = WebFetchTool()
        result = tool.execute()
        assert result.error is not None
