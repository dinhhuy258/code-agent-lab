"""ActivateSkillTool -- LLM tool for activating skills."""

from code_agent.llm.types import ToolDeclaration
from code_agent.skills.skill_manager import SkillManager
from code_agent.tools.base import BaseTool, ToolResult


class ActivateSkillTool(BaseTool):
    """Tool that lets the model activate a skill to receive its instructions."""

    def __init__(self, skill_manager: SkillManager) -> None:
        self._skill_manager = skill_manager

    def get_name(self) -> str:
        return "activate_skill"

    def get_declaration(self) -> ToolDeclaration:
        skill_names = [s.name for s in self._skill_manager.get_skills()]
        return ToolDeclaration(
            name="activate_skill",
            description=(
                "Activate a skill to receive its detailed instructions. "
                "Call this when you determine a skill is relevant to the user's request."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "skill_name": {
                        "type": "string",
                        "description": "The name of the skill to activate.",
                        "enum": skill_names,
                    },
                },
                "required": ["skill_name"],
            },
        )

    def execute(self, **kwargs) -> ToolResult:
        name: str = kwargs.get("skill_name", "")
        skill = self._skill_manager.activate_skill(name)
        if skill is None:
            available = ", ".join(s.name for s in self._skill_manager.get_skills())
            return ToolResult(
                content="",
                error=f"Skill '{name}' not found. Available skills: {available}",
            )

        return ToolResult(
            content=(
                f'<activated_skill name="{skill.name}">\n'
                f"<instructions>\n{skill.body}\n</instructions>\n"
                f"</activated_skill>"
            )
        )

    def needs_confirmation(self, **kwargs) -> bool:
        return False
