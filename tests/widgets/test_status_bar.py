from textual.app import App, ComposeResult

from code_agent.widgets.status_bar import StatusBar


class StatusBarTestApp(App[None]):
    def compose(self) -> ComposeResult:
        yield StatusBar(model_name="gemini-2.5-flash")


async def test_status_bar_shows_model_name() -> None:
    async with StatusBarTestApp().run_test() as pilot:
        app = pilot.app
        bar = app.query_one(StatusBar)
        rendered = str(bar.render())
        assert "gemini-2.5-flash" in rendered


async def test_status_bar_shows_tokens_after_usage() -> None:
    async with StatusBarTestApp().run_test() as pilot:
        app = pilot.app
        bar = app.query_one(StatusBar)
        bar.add_usage(prompt_tokens=1000, candidates_tokens=500, total_tokens=1500)
        rendered = str(bar.render())
        assert "1,000" in rendered
        assert "500" in rendered


async def test_status_bar_shows_cost_estimate() -> None:
    async with StatusBarTestApp().run_test() as pilot:
        app = pilot.app
        bar = app.query_one(StatusBar)
        bar.add_usage(prompt_tokens=1000, candidates_tokens=500, total_tokens=1500)
        rendered = str(bar.render())
        assert "$" in rendered
