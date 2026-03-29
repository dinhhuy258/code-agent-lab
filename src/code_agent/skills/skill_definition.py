"""SkillDefinition dataclass."""

from dataclasses import dataclass


@dataclass
class SkillDefinition:
    """A discovered skill parsed from a SKILL.md file."""

    name: str
    description: str
    body: str
    location: str
