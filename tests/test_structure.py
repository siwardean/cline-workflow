"""
Structural tests — verify files exist, frontmatter is valid, required
sections are present, and Cursor rules have alwaysApply: true.
"""

import pytest
import yaml
from pathlib import Path
from helpers import (
    REPO_ROOT,
    WORKFLOWS,
    TOOL_WORKFLOW_DIRS,
    TOOL_RULES_FILES,
    TOOL_EXTENSIONS,
    workflow_path,
    read_frontmatter,
    workflow_params,
)


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tool,workflow", workflow_params())
def test_workflow_file_exists(tool, workflow):
    path = workflow_path(tool, workflow)
    assert path.exists(), f"Missing: {path.relative_to(REPO_ROOT)}"


@pytest.mark.parametrize("tool,rules_file", TOOL_RULES_FILES.items())
def test_rules_file_exists(tool, rules_file):
    assert rules_file.exists(), f"Missing rules file for {tool}: {rules_file.relative_to(REPO_ROOT)}"


def test_memory_bank_current_mr_exists():
    assert (REPO_ROOT / "memory-bank" / "current-mr.md").exists()


def test_claude_md_exists():
    assert (REPO_ROOT / "CLAUDE.md").exists()


# ---------------------------------------------------------------------------
# Frontmatter validity
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tool,workflow", workflow_params())
def test_frontmatter_is_valid_yaml(tool, workflow):
    """Frontmatter block must be parseable YAML."""
    path = workflow_path(tool, workflow)
    content = path.read_text()
    if not content.startswith("---"):
        pytest.skip("No frontmatter block")
    end = content.index("---", 3)
    raw = content[3:end]
    parsed = yaml.safe_load(raw)  # raises on invalid YAML
    assert isinstance(parsed, dict), "Frontmatter must parse to a dict"


@pytest.mark.parametrize("tool,workflow", workflow_params())
def test_frontmatter_has_name_and_description(tool, workflow):
    path = workflow_path(tool, workflow)
    fm = read_frontmatter(path)
    if not fm:
        pytest.skip("No frontmatter")
    assert "name" in fm, f"{path.name}: frontmatter missing 'name'"
    assert "description" in fm, f"{path.name}: frontmatter missing 'description'"


# ---------------------------------------------------------------------------
# Cursor-specific: alwaysApply
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("workflow", WORKFLOWS)
def test_cursor_workflow_has_always_apply_false(workflow):
    """Workflow files are on-demand — alwaysApply must be false to avoid
    loading the full workflow instructions into every chat context."""
    path = workflow_path("cursor", workflow)
    fm = read_frontmatter(path)
    assert fm.get("alwaysApply") is False, \
        f"{path.name}: cursor workflow files must have 'alwaysApply: false'"


def test_cursor_rules_mdc_has_always_apply():
    fm = read_frontmatter(TOOL_RULES_FILES["cursor"])
    assert fm.get("alwaysApply") is True, \
        "cursor rules.mdc must have 'alwaysApply: true'"


# ---------------------------------------------------------------------------
# Required sections in each workflow
# ---------------------------------------------------------------------------

REQUIRED_SECTIONS = {
    "start":   ["## Steps", "## What This Workflow Does"],
    "morning": ["## Steps", "## What This Workflow Does", "## Phase 1", "## Phase 2"],
    "commit":  ["## Steps", "## What This Workflow Does"],
    "close":   ["## Steps", "## What This Workflow Does"],
}


@pytest.mark.parametrize("tool,workflow", workflow_params())
def test_workflow_has_required_sections(tool, workflow):
    path = workflow_path(tool, workflow)
    content = path.read_text()
    for section in REQUIRED_SECTIONS.get(workflow, []):
        assert section in content, \
            f"{path.relative_to(REPO_ROOT)}: missing section '{section}'"


# ---------------------------------------------------------------------------
# Required sections in rules files
# ---------------------------------------------------------------------------

REQUIRED_RULES_SECTIONS = [
    "## Branch naming",
    "## Commits",
    "## SonarQube",
    "## Workflow execution",
]


@pytest.mark.parametrize("tool,rules_file", TOOL_RULES_FILES.items())
def test_rules_file_has_required_sections(tool, rules_file):
    content = rules_file.read_text()
    for section in REQUIRED_RULES_SECTIONS:
        assert section in content, \
            f"{rules_file.relative_to(REPO_ROOT)}: missing section '{section}'"


# ---------------------------------------------------------------------------
# Workflows README
# ---------------------------------------------------------------------------

def test_workflows_readme_exists():
    readme = REPO_ROOT / ".clinerules" / "workflows" / "README.md"
    assert readme.exists(), "Missing .clinerules/workflows/README.md"


def test_workflows_readme_covers_all_workflows():
    readme = REPO_ROOT / ".clinerules" / "workflows" / "README.md"
    content = readme.read_text()
    for wf in WORKFLOWS:
        assert f"{wf}.md" in content, \
            f"workflows/README.md does not mention {wf}.md"
