from code_agent.widgets.thinking_indicator import ThinkingIndicator


class TestThinkingIndicator:
    def test_tick_updates_elapsed(self) -> None:
        indicator = ThinkingIndicator()
        indicator._tick()
        assert indicator._elapsed == 1
        assert indicator._frame == 1

    def test_tick_cycles_spinner_frames(self) -> None:
        indicator = ThinkingIndicator()
        for _ in range(len(ThinkingIndicator.SPINNER_FRAMES)):
            indicator._tick()
        assert indicator._frame == 0  # wraps around

    def test_minute_format(self) -> None:
        indicator = ThinkingIndicator()
        indicator._elapsed = 59
        indicator._tick()
        assert indicator._elapsed == 60
