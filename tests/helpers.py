"""Shared fixtures and helpers for workflow tests."""

import re
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

# All workflow names (no extension)
WORKFLOWS = ["start", "morning", "commit", "review", "close"]

# Paths per tool
TOOL_WORKFLOW_DIRS = {
    "cline":      REPO_ROOT / ".clinerules" / "workflows",
    "kilocode":   REPO_ROOT / ".kilocoderules" / "workflows",
    "cursor":     REPO_ROOT / ".cursor" / "rules",
    "claude_code": REPO_ROOT / ".claude" / "commands",
}

TOOL_RULES_FILES = {
    "cline":      REPO_ROOT / ".clinerules" / "rules.md",
    "kilocode":   REPO_ROOT / ".kilocoderules" / "rules.md",
    "cursor":     REPO_ROOT / ".cursor" / "rules" / "rules.mdc",
    "claude_code": REPO_ROOT / "CLAUDE.md",
}

# Expected file extension per tool
TOOL_EXTENSIONS = {
    "cline":      ".md",
    "kilocode":   ".md",
    "cursor":     ".mdc",
    "claude_code": ".md",
}


def workflow_path(tool: str, workflow: str) -> Path:
    ext = TOOL_EXTENSIONS[tool]
    return TOOL_WORKFLOW_DIRS[tool] / f"{workflow}{ext}"


def read_frontmatter(path: Path) -> dict:
    """Parse YAML frontmatter between --- delimiters. Returns {} if none."""
    import yaml
    content = path.read_text()
    if not content.startswith("---"):
        return {}
    end = content.index("---", 3)
    return yaml.safe_load(content[3:end]) or {}


def workflow_params():
    """pytest params for (tool, workflow) combinations."""
    return [
        pytest.param(tool, wf, id=f"{tool}/{wf}")
        for tool in TOOL_WORKFLOW_DIRS
        for wf in WORKFLOWS
    ]
