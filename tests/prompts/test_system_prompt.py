"""Tests for prompt snippet renderers.

"""

from code_agent.prompts.system_prompt import (
    UserContext,
    compose_system_prompt,
    get_core_system_prompt,
    render_core_mandates,
    render_operational_guidelines,
    render_preamble,
    render_user_context,
)

class TestRenderPreamble:
    def test_returns_interactive_preamble(self) -> None:
        result = render_preamble()
        assert "interactive" in result.lower()
        assert "code agent" in result.lower()

class TestRenderCoreMandates:
    def test_includes_security_section(self) -> None:
        result = render_core_mandates()
        assert "Security" in result

    def test_includes_context_efficiency(self) -> None:
        result = render_core_mandates()
        assert "Context Efficiency" in result

    def test_includes_engineering_standards(self) -> None:
        result = render_core_mandates()
        assert "Engineering Standards" in result

class TestRenderOperationalGuidelines:
    def test_includes_tone_and_style(self) -> None:
        result = render_operational_guidelines()
        assert "Tone" in result

    def test_includes_security_rules(self) -> None:
        result = render_operational_guidelines()
        assert "Security" in result

    def test_includes_tool_usage(self) -> None:
        result = render_operational_guidelines()
        assert "Tool Usage" in result

class TestRenderUserContext:
    def test_none_returns_empty(self) -> None:
        assert render_user_context(None) == ""

    def test_global_only(self) -> None:
        ctx = UserContext(global_context="Global prefs")
        result = render_user_context(ctx)
        assert "<global_context>" in result
        assert "Global prefs" in result

    def test_all_sections(self) -> None:
        ctx = UserContext(
            global_context="Global prefs",
            project_context="Project rules",
        )
        result = render_user_context(ctx)
        assert "<global_context>" in result
        assert "<project_context>" in result
        assert "Contextual Instructions" in result

    def test_empty_returns_empty(self) -> None:
        ctx = UserContext()
        assert render_user_context(ctx) == ""

class TestComposeSystemPrompt:
    def test_wraps_base_prompt_with_context(self) -> None:
        ctx = UserContext(project_context="Project rules")
        result = compose_system_prompt("Base prompt here.", ctx)
        assert "Base prompt here." in result
        assert "Project rules" in result

    def test_no_context_returns_base_prompt(self) -> None:
        result = compose_system_prompt("Base prompt here.")
        assert result.strip() == "Base prompt here."

class TestGetCoreSystemPrompt:
    def test_composes_all_sections(self) -> None:
        result = get_core_system_prompt()
        assert "code agent" in result.lower()
        assert "Security" in result
        assert "Operational Guidelines" in result
