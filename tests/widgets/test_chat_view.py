from textual.app import App, ComposeResult

from code_agent.widgets.chat_view import ChatView
from code_agent.widgets.message import AgentMessage, UserMessage

class ChatViewTestApp(App[None]):
    def compose(self) -> ComposeResult:
        yield ChatView()

async def test_chat_view_mount_messages() -> None:
    async with ChatViewTestApp().run_test() as pilot:
        app = pilot.app
        chat_view = app.query_one(ChatView)
        await chat_view.mount(UserMessage("Test message"))
        await chat_view.mount(AgentMessage("Test response"))
        user_msgs = app.query(UserMessage)
        agent_msgs = app.query(AgentMessage)
        assert len(user_msgs) == 1
        assert len(agent_msgs) == 1
