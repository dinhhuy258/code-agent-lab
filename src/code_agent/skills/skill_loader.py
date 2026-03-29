"""Skill file discovery and parsing."""

import logging
import re
from pathlib import Path

import yaml

from code_agent.skills.skill_definition import SkillDefinition

logger = logging.getLogger(__name__)

_FRONTMATTER_RE = re.compile(r"^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n([\s\S]*)?)?")


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from a SKILL.md file.

    Returns:
        A tuple of (metadata dict, body string).
    """
    match = _FRONTMATTER_RE.match(content)
    if not match:
        return {}, content

    raw_yaml = match.group(1)
    body = match.group(2) or ""

    try:
        meta = yaml.safe_load(raw_yaml)
        if not isinstance(meta, dict):
            return {}, content
    except yaml.YAMLError:
        logger.warning("Failed to parse YAML frontmatter: %s", raw_yaml[:100])
        return {}, content

    return meta, body


def load_skill_from_file(file_path: Path) -> SkillDefinition | None:
    """Load a single SkillDefinition from a SKILL.md file.

    Returns None if the file cannot be read.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError:
        logger.warning("Cannot read skill file: %s", file_path)
        return None

    meta, body = parse_frontmatter(content)
    name = meta.get("name") or file_path.parent.name
    description = meta.get("description", "") or ""

    return SkillDefinition(
        name=str(name),
        description=str(description),
        body=body.strip(),
        location=str(file_path),
    )


def load_skills_from_dir(dir_path: Path) -> list[SkillDefinition]:
    """Discover and load all SKILL.md files from a directory.

    Looks for SKILL.md at the top level and one level deep (*/SKILL.md).
    Returns an empty list if the directory does not exist.
    """
    if not dir_path.is_dir():
        return []

    skills: list[SkillDefinition] = []

    # Top-level SKILL.md
    top_level = dir_path / "SKILL.md"
    if top_level.is_file():
        skill = load_skill_from_file(top_level)
        if skill is not None:
            skills.append(skill)

    # Subdirectory SKILL.md files
    for child in sorted(dir_path.iterdir()):
        if not child.is_dir():
            continue
        if child.name in ("node_modules", ".git"):
            continue
        skill_file = child / "SKILL.md"
        if skill_file.is_file():
            skill = load_skill_from_file(skill_file)
            if skill is not None:
                skills.append(skill)

    return skills
