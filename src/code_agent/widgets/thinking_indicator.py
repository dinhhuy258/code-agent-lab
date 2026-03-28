"""ThinkingIndicator — shows a spinner and elapsed time while waiting for LLM response.

# Ref: gemini-cli LoadingIndicator (packages/cli/src/ui/components/LoadingIndicator.tsx)
# Ref: gemini-cli useTimer (packages/cli/src/ui/hooks/useTimer.ts)
"""

from textual.widgets import Static


class ThinkingIndicator(Static):
    """Displays an animated spinner with elapsed time."""

    DEFAULT_CSS = """
    ThinkingIndicator {
        margin: 1 2 0 0;
        padding: 1 2;
        color: $text-muted;
    }
    """

    SPINNER_FRAMES = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")

    def __init__(self) -> None:
        super().__init__("⠋ Thinking... 0s")
        self._elapsed = 0
        self._frame = 0

    def on_mount(self) -> None:
        self.set_interval(1.0, self._tick)

    def _tick(self) -> None:
        self._elapsed += 1
        self._frame = (self._frame + 1) % len(self.SPINNER_FRAMES)
        spinner = self.SPINNER_FRAMES[self._frame]
        if self._elapsed < 60:
            time_str = f"{self._elapsed}s"
        else:
            minutes = self._elapsed // 60
            seconds = self._elapsed % 60
            time_str = f"{minutes}m {seconds}s"
        self.update(f"{spinner} Thinking... {time_str}")
