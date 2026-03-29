from textual.app import App, ComposeResult

from code_agent.widgets.message_input import MessageInput


class InputTestApp(App[None]):
    def compose(self) -> ComposeResult:
        yield MessageInput()


async def test_message_input_renders() -> None:
    async with InputTestApp().run_test() as pilot:
        app = pilot.app
        widget = app.query_one(MessageInput)
        assert widget is not None
        assert widget.border_title == "Message"


async def test_message_input_has_border_subtitle() -> None:
    async with InputTestApp().run_test() as pilot:
        app = pilot.app
        widget = app.query_one(MessageInput)
        assert widget.border_subtitle == "\\ + enter for newline"


async def test_message_input_submit_clears_text() -> None:
    async with InputTestApp().run_test() as pilot:
        app = pilot.app
        widget = app.query_one(MessageInput)
        widget.focus()
        widget.text = "Hello world"
        await pilot.press("enter")
        await pilot.pause()
        assert widget.text == ""


async def test_message_input_submit_empty_ignored() -> None:
    """Submitting empty or whitespace-only text should not post a message."""
    messages: list = []

    class TrackingApp(App[None]):
        def compose(self) -> ComposeResult:
            yield MessageInput()

        def on_message_input_submitted(self, event: MessageInput.Submitted) -> None:
            messages.append(event.text)

    async with TrackingApp().run_test() as pilot:
        app = pilot.app
        widget = app.query_one(MessageInput)
        widget.focus()
        widget.text = "   "
        await pilot.press("enter")
        await pilot.pause()
        assert len(messages) == 0
