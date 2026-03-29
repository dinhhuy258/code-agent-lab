"""StatusBar -- displays model name, token usage, and cost estimate."""

from textual.widgets import Static

# Approximate cost per million tokens (input/output) for common models.
# Used for rough estimates only.
COST_PER_MILLION_INPUT = 0.15   # $0.15 per 1M input tokens (Gemini 2.5 Flash)
COST_PER_MILLION_OUTPUT = 0.60  # $0.60 per 1M output tokens


class StatusBar(Static):
    """Displays session status: model name, token usage, and cost estimate."""

    def __init__(self, model_name: str = "") -> None:
        self._model_name = model_name
        self._prompt_tokens = 0
        self._cached_tokens = 0
        self._candidates_tokens = 0
        self._thoughts_tokens = 0
        self._total_tokens = 0
        super().__init__(self._build_text(), classes="status-bar")

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
        self.update(self._build_text())

    def _estimate_cost(self) -> float:
        """Estimate cost in USD based on token counts."""
        input_cost = (self._prompt_tokens / 1_000_000) * COST_PER_MILLION_INPUT
        output_cost = (self._candidates_tokens / 1_000_000) * COST_PER_MILLION_OUTPUT
        return input_cost + output_cost

    def _build_text(self) -> str:
        """Build the status bar text."""
        parts: list[str] = []

        if self._model_name:
            parts.append(self._model_name)

        tokens = f"{self._prompt_tokens:,}↑ {self._candidates_tokens:,}↓"
        if self._cached_tokens:
            tokens += f" {self._cached_tokens:,}⚡"
        if self._thoughts_tokens:
            tokens += f" {self._thoughts_tokens:,}💭"
        parts.append(tokens)

        cost = self._estimate_cost()
        if cost >= 0.01:
            parts.append(f"${cost:.3f}")
        elif cost > 0:
            parts.append(f"${cost:.4f}")
        else:
            parts.append("$0.00")

        return "  │  ".join(parts)
