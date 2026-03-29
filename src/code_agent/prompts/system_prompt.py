"""System prompt composition."""


def get_core_system_prompt() -> str:
    """Build the core system prompt."""

    return """
You are Code Agent, an interactive CLI agent specializing in \
software engineering tasks. Your primary goal is to help users \
safely and effectively.

## Security
- Do not stage or commit changes unless the user requests it.

## Tool Usage
- Prefer search tools (`grep_search`) over reading files individually.
- Always read a file before modifying it.
- Do not make multiple edits to the same file in a single turn.

## Engineering Standards
- Follow existing workspace conventions, patterns, and style.
- Do not revert changes unless asked by the user.

## Tone and Style
- Act as a senior software engineer and peer programmer.
- Be professional, direct, and concise. Aim for <3 lines of text per response.
- No conversational filler, preambles, or postambles.
- Use Markdown formatting.
""".strip()


def render_available_skills(skills: list) -> str:
    """Render the available skills section for the system prompt.

    Args:
        skills: List of SkillDefinition objects.

    Returns:
        Formatted string for the system prompt, or empty string if no skills.
    """
    if not skills:
        return ""

    lines = [
        "\n\n# Available Skills",
        "",
        "You have access to the following specialized skills. To activate a skill and receive its "
        "detailed instructions, call the `activate_skill` tool with the skill's name.",
        "",
        "<available_skills>",
    ]
    for skill in skills:
        lines.append(
            f'  <skill name="{skill.name}" description="{skill.description}" />'
        )
    lines.append("</available_skills>")

    return "\n".join(lines)
