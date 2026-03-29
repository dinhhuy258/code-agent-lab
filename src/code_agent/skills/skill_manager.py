"""SkillManager -- discovers, registers, and activates skills."""

import logging
from pathlib import Path

from code_agent.skills.skill_definition import SkillDefinition
from code_agent.skills.skill_loader import load_skills_from_dir

logger = logging.getLogger(__name__)


class SkillManager:
    """Central registry for skills discovered from the workspace."""

    def __init__(self, workspace_dir: Path) -> None:
        self._workspace_dir = workspace_dir
        self._skills: dict[str, SkillDefinition] = {}
        self._active_skills: set[str] = set()

    def discover_skills(self) -> None:
        """Discover skills from .code-agent/skills/ in the workspace."""
        self._skills.clear()
        self._active_skills.clear()

        skills_dir = self._workspace_dir / ".code-agent" / "skills"
        skills = load_skills_from_dir(skills_dir)

        for skill in skills:
            if skill.name in self._skills:
                logger.warning(
                    "Duplicate skill name '%s', overriding with %s",
                    skill.name,
                    skill.location,
                )
            self._skills[skill.name] = skill

        if self._skills:
            logger.info(
                "Discovered %d skill(s): %s",
                len(self._skills),
                ", ".join(self._skills.keys()),
            )

    def get_skills(self) -> list[SkillDefinition]:
        """Return all discovered skills."""
        return list(self._skills.values())

    def get_skill(self, name: str) -> SkillDefinition | None:
        """Look up a skill by name."""
        return self._skills.get(name)

    def activate_skill(self, name: str) -> SkillDefinition | None:
        """Mark a skill as active and return its definition.

        Returns None if the skill is not found.
        """
        skill = self._skills.get(name)
        if skill is None:
            return None
        self._active_skills.add(name)
        return skill

    def is_skill_active(self, name: str) -> bool:
        """Check if a skill is currently active."""
        return name in self._active_skills
