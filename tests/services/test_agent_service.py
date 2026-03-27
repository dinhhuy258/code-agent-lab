from code_agent.services.agent_service import AgentService


class TestAgentService:
    def test_send_returns_string(self) -> None:
        service = AgentService()
        response = service.send("Hello")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_send_includes_user_text(self) -> None:
        service = AgentService()
        response = service.send("What is Python?")
        assert "What is Python?" in response

    def test_history_tracks_messages(self) -> None:
        service = AgentService()
        service.send("First message")
        service.send("Second message")
        history = service.get_history()
        assert len(history) == 4  # 2 user + 2 agent
        assert history[0] == {"role": "user", "content": "First message"}
        assert history[1]["role"] == "agent"
        assert history[2] == {"role": "user", "content": "Second message"}
        assert history[3]["role"] == "agent"
