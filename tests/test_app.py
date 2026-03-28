from textual.widgets import Input

from code_agent.app import CodeAgentApp
from code_agent.llm.types import GenerateContentRequest, TurnResult
from code_agent.widgets.message import AgentMessage, UserMessage


class FakeLLMClient:
    """Fake LLM client for testing -- returns canned responses."""

    def __init__(self, responses: list[str] | None = None) -> None:
        self._responses = iter(responses or ["Mock response."])

    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        return TurnResult(text=next(self._responses))


async def _type_and_submit(pilot, text: str) -> None:
    """Type text into the focused input and press enter."""
    for char in text:
        await pilot.press(char)
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


def _make_app(responses: list[str] | None = None) -> CodeAgentApp:
    """Create a CodeAgentApp with a fake LLM client."""
    return CodeAgentApp(llm_client=FakeLLMClient(responses or ["Mock response."]))


async def test_send_message_creates_widgets() -> None:
    async with _make_app(["Hello!"]).run_test() as pilot:
        app = pilot.app
        await _type_and_submit(pilot, "Hello agent")
        await app.workers.wait_for_complete()
        await pilot.pause()
        user_msgs = app.query(UserMessage)
        agent_msgs = app.query(AgentMessage)
        assert len(user_msgs) == 1
        assert len(agent_msgs) == 1


async def test_empty_input_ignored() -> None:
    async with _make_app().run_test() as pilot:
        app = pilot.app
        app.query_one(Input).value = "   "
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        user_msgs = app.query(UserMessage)
        assert len(user_msgs) == 0


async def test_multiple_messages() -> None:
    async with _make_app(["R1", "R2", "R3"]).run_test() as pilot:
        app = pilot.app
        for msg in ["First", "Second", "Third"]:
            await _type_and_submit(pilot, msg)
            await app.workers.wait_for_complete()
            await pilot.pause()
        user_msgs = app.query(UserMessage)
        agent_msgs = app.query(AgentMessage)
        assert len(user_msgs) == 3
        assert len(agent_msgs) == 3


async def test_no_api_key_shows_error() -> None:
    async with CodeAgentApp(llm_client=None).run_test() as pilot:
        app = pilot.app
        await _type_and_submit(pilot, "Hello")
        agent_msgs = app.query(AgentMessage)
        assert len(agent_msgs) == 1
