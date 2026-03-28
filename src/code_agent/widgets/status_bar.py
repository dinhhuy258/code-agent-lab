from textual.widgets import Static


class StatusBar(Static):
    """Displays session status information including token usage."""

    def __init__(self) -> None:
        super().__init__("Tokens: 0 in / 0 out / 0 total", classes="status-bar")
        self._prompt_tokens = 0
        self._cached_tokens = 0
        self._candidates_tokens = 0
        self._thoughts_tokens = 0
        self._total_tokens = 0

    def add_usage(
        self,
        prompt_tokens: int,
        candidates_tokens: int,
        total_tokens: int,
        cached_tokens: int = 0,
        thoughts_tokens: int = 0,
    ) -> None:
        """Accumulate token usage from a turn and update the display."""
        self._prompt_tokens += prompt_tokens
        self._cached_tokens += cached_tokens
        self._candidates_tokens += candidates_tokens
        self._thoughts_tokens += thoughts_tokens
        self._total_tokens += total_tokens
        self._render_status()

    def _render_status(self) -> None:
        """Re-render the status bar content."""
        parts = [
            f"Tokens: {self._prompt_tokens:,} in",
            f"{self._candidates_tokens:,} out",
        ]
        if self._cached_tokens:
            parts.append(f"{self._cached_tokens:,} cached")
        if self._thoughts_tokens:
            parts.append(f"{self._thoughts_tokens:,} thinking")
        parts.append(f"{self._total_tokens:,} total")
        self.update(" / ".join(parts))
