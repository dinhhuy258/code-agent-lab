from textual.widgets import Input

from code_agent.app import CodeAgentApp
from code_agent.widgets.message import AgentMessage, UserMessage


async def _type_and_submit(pilot, text: str) -> None:
    """Type text into the focused input and press enter."""
    for char in text:
        await pilot.press(char)
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


async def test_send_message_creates_widgets() -> None:
    async with CodeAgentApp().run_test() as pilot:
        app = pilot.app
        await _type_and_submit(pilot, "Hello agent")
        user_msgs = app.query(UserMessage)
        agent_msgs = app.query(AgentMessage)
        assert len(user_msgs) == 1
        assert len(agent_msgs) == 1


async def test_empty_input_ignored() -> None:
    async with CodeAgentApp().run_test() as pilot:
        app = pilot.app
        app.query_one(Input).value = "   "
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        user_msgs = app.query(UserMessage)
        assert len(user_msgs) == 0


async def test_multiple_messages() -> None:
    async with CodeAgentApp().run_test() as pilot:
        app = pilot.app
        for msg in ["First", "Second", "Third"]:
            await _type_and_submit(pilot, msg)
        user_msgs = app.query(UserMessage)
        agent_msgs = app.query(AgentMessage)
        assert len(user_msgs) == 3
        assert len(agent_msgs) == 3
