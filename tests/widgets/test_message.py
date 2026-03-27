from textual.app import App, ComposeResult

from code_agent.widgets.message import AgentMessage, UserMessage


class MessageTestApp(App[None]):
    def compose(self) -> ComposeResult:
        yield UserMessage("Hello from user")
        yield AgentMessage("Hello from agent")


async def test_user_message_renders() -> None:
    async with MessageTestApp().run_test() as pilot:
        app = pilot.app
        user_msg = app.query_one(UserMessage)
        assert "Hello from user" in str(user_msg.render())
        assert user_msg.has_class("user-message")


async def test_agent_message_renders() -> None:
    async with MessageTestApp().run_test() as pilot:
        app = pilot.app
        agent_msg = app.query_one(AgentMessage)
        assert "Hello from agent" in str(agent_msg.render())
        assert agent_msg.has_class("agent-message")
