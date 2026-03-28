from code_agent.core.agent_client import AgentClient
from code_agent.llm.types import GenerateContentRequest, TurnResult


class FakeLLMClient:
    def __init__(self, responses: list[str]) -> None:
        self._responses = iter(responses)

    def generate_content(self, request: GenerateContentRequest) -> TurnResult:
        return TurnResult(text=next(self._responses))


class TestAgentClient:
    def test_send_returns_response_text(self) -> None:
        client = FakeLLMClient(["Hello from agent!"])
        agent = AgentClient(client=client)
        response = agent.send("Hi")
        assert response == "Hello from agent!"

    def test_send_preserves_conversation(self) -> None:
        client = FakeLLMClient(["R1", "R2"])
        agent = AgentClient(client=client)
        agent.send("M1")
        response = agent.send("M2")
        assert response == "R2"

    def test_system_instruction_forwarded(self) -> None:
        requests: list[GenerateContentRequest] = []

        class CapturingClient:
            def generate_content(self, request: GenerateContentRequest) -> TurnResult:
                requests.append(request)
                return TurnResult(text="ok")

        agent = AgentClient(
            client=CapturingClient(),
            system_instruction="Be concise.",
        )
        agent.send("Hi")
        assert requests[0].system_instruction == "Be concise."
