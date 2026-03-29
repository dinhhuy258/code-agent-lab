"""Application configuration."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    """Configuration parsed from CLI arguments."""

    debug_dir: Path | None = None
