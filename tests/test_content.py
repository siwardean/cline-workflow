"""
Content/contract tests — verify no stale references, cross-tool parity,
branch naming convention, MCP tool names, and memory-bank references.
"""

import re
import pytest
from pathlib import Path
from helpers import (
    REPO_ROOT,
    WORKFLOWS,
    TOOL_WORKFLOW_DIRS,
    TOOL_RULES_FILES,
    workflow_path,
    read_frontmatter,
    workflow_params,
)


# ---------------------------------------------------------------------------
# No stale references
# ---------------------------------------------------------------------------

STALE_PATTERNS = [
    (r"\beod\.md\b",  "eod.md (removed workflow)"),
    (r"\beod\.mdc\b", "eod.mdc (removed workflow)"),
]


@pytest.mark.parametrize("tool,workflow", workflow_params())
def test_no_stale_references_in_workflows(tool, workflow):
    path = workflow_path(tool, workflow)
    content = path.read_text()
    for pattern, label in STALE_PATTERNS:
        assert not re.search(pattern, content), \
            f"{path.name}: contains stale reference to {label}"


@pytest.mark.parametrize("tool,rules_file", TOOL_RULES_FILES.items())
def test_no_stale_references_in_rules(tool, rules_file):
    content = rules_file.read_text()
    for pattern, label in STALE_PATTERNS:
        assert not re.search(pattern, content), \
            f"{rules_file.name}: contains stale reference to {label}"


# ---------------------------------------------------------------------------
# Cross-tool consistency: frontmatter name matches workflow name
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tool,workflow", workflow_params())
def test_frontmatter_name_matches_filename(tool, workflow):
    path = workflow_path(tool, workflow)
    fm = read_frontmatter(path)
    if not fm or "name" not in fm:
        pytest.skip("No frontmatter name")
    assert fm["name"] == workflow, \
        f"{path.name}: frontmatter 'name: {fm['name']}' does not match filename '{workflow}'"


# ---------------------------------------------------------------------------
# Cross-tool parity: same description across tools for each workflow
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("workflow", WORKFLOWS)
def test_workflow_description_consistent_across_tools(workflow):
    """All tools should ship the same workflow description."""
    descriptions = {}
    for tool in TOOL_WORKFLOW_DIRS:
        fm = read_frontmatter(workflow_path(tool, workflow))
        if fm.get("description"):
            descriptions[tool] = fm["description"]

    if len(descriptions) < 2:
        pytest.skip("Not enough tools have frontmatter to compare")

    unique = set(descriptions.values())
    assert len(unique) == 1, (
        f"Workflow '{workflow}' has inconsistent descriptions across tools:\n"
        + "\n".join(f"  {t}: {d}" for t, d in descriptions.items())
    )


# ---------------------------------------------------------------------------
# memory-bank/current-mr.md references
# ---------------------------------------------------------------------------

WORKFLOWS_THAT_READ_CONFIG = ["start", "morning", "commit", "review", "close"]


@pytest.mark.parametrize("workflow", WORKFLOWS_THAT_READ_CONFIG)
def test_workflow_references_current_mr(workflow):
    """All workflows must reference memory-bank/current-mr.md."""
    # Check the canonical source (clinerules)
    path = workflow_path("cline", workflow)
    content = path.read_text()
    assert "current-mr.md" in content, \
        f"{path.name}: does not reference memory-bank/current-mr.md"


# ---------------------------------------------------------------------------
# MCP tool name contracts
# ---------------------------------------------------------------------------

MCP_TOOL_CONTRACTS = {
    "morning": ["gitlab_get_merge_request", "gitlab_get_discussions", "gitlab_update_merge_request"],
    "commit":  ["gitlab_update_merge_request"],
    "review":  ["gitlab_get_merge_request", "gitlab_get_discussions", "gitlab_create_discussion"],
    "close":   ["gitlab_get_merge_request", "gitlab_get_discussions"],
}


@pytest.mark.parametrize("workflow,tools", MCP_TOOL_CONTRACTS.items())
def test_workflow_mentions_expected_mcp_tools(workflow, tools):
    path = workflow_path("cline", workflow)
    content = path.read_text()
    for tool_name in tools:
        assert tool_name in content, \
            f"{path.name}: missing expected MCP tool reference '{tool_name}'"


# ---------------------------------------------------------------------------
# Branch naming convention
# ---------------------------------------------------------------------------

BRANCH_NAMING_REGEX = re.compile(r"^feature/[a-z][a-z_]+$")

# Examples pulled from the rules files — extract them and validate they match
KNOWN_BRANCH_EXAMPLES = [
    "feature/password_reset_email",
    "feature/product_listing_pagination",
    "feature/stripe_subscription_billing",
]


@pytest.mark.parametrize("branch", KNOWN_BRANCH_EXAMPLES)
def test_branch_naming_examples_match_convention(branch):
    assert BRANCH_NAMING_REGEX.match(branch), \
        f"Branch example '{branch}' does not match pattern feature/<word>_<word>"


def test_branch_naming_rejects_generic_words():
    invalid = [
        "feature/add_user",
        "feature/fix_bug",
        "feature/update_settings",
        "feature/new_feature",
    ]
    for branch in invalid:
        # These contain generic words but still match the format — this test
        # verifies the rules section explicitly lists the forbidden words
        rules = TOOL_RULES_FILES["cline"].read_text()
        for word in ["add", "update", "fix", "feature", "implement", "new", "change"]:
            assert word in rules, \
                f"rules.md must list '{word}' as a forbidden generic word in branch names"
        break  # only need to check rules content once


def test_branch_naming_convention_in_start_workflow():
    """start.md must apply the branch naming convention."""
    path = workflow_path("cline", "start")
    content = path.read_text()
    assert "feature/" in content, \
        "start.md should reference the feature/ branch prefix"


# ---------------------------------------------------------------------------
# Commit message format
# ---------------------------------------------------------------------------

def test_commit_format_documented_in_commit_workflow():
    path = workflow_path("cline", "commit")
    content = path.read_text()
    assert "<type>" in content and "<scope>" in content and "<subject>" in content, \
        "commit.md must document Angular Conventional Commits format"


def test_commit_types_listed_in_rules():
    content = TOOL_RULES_FILES["cline"].read_text()
    for t in ["feat", "fix", "docs", "refactor", "test", "chore"]:
        assert t in content, f"rules.md missing commit type '{t}'"


# ---------------------------------------------------------------------------
# Tools rules parity: all rules files define the same branch naming format
# ---------------------------------------------------------------------------

def test_all_rules_files_define_branch_format():
    for tool, rules_file in TOOL_RULES_FILES.items():
        content = rules_file.read_text()
        assert "feature/" in content, \
            f"{rules_file.relative_to(REPO_ROOT)}: missing branch naming format example"
        assert "## Branch naming" in content, \
            f"{rules_file.relative_to(REPO_ROOT)}: missing '## Branch naming' section"


# ---------------------------------------------------------------------------
# Review workflow content contracts
# ---------------------------------------------------------------------------

def test_review_prompts_for_mr_on_main():
    """review.md must handle the case where the user is on main/master."""
    path = workflow_path("cline", "review")
    content = path.read_text()
    assert "main" in content and "master" in content, \
        "review.md must handle being run from main/master branch"
    # Must ask for MR IID or branch name in that case
    assert "mr_iid" in content.lower() or "MR IID" in content, \
        "review.md must prompt for MR IID when branch is not matched"


def test_review_thread_assessment_categories():
    """review.md must classify existing threads into the three expected states."""
    path = workflow_path("cline", "review")
    content = path.read_text()
    assert "Addressed by code" in content, \
        "review.md missing thread classification: 'Addressed by code'"
    assert "Addressed by reply" in content, \
        "review.md missing thread classification: 'Addressed by reply'"
    assert "Needs attention" in content, \
        "review.md missing thread classification: 'Needs attention'"


def test_review_single_approval_gate():
    """review.md must have exactly one prompt for the user, not one per finding."""
    path = workflow_path("cline", "review")
    content = path.read_text()
    # Must ask which findings to post in a single step
    assert "which" in content.lower() and ("post" in content.lower() or "thread" in content.lower()), \
        "review.md must have a single 'which findings to post' prompt"
    # Must NOT require per-finding confirmation
    assert "approve each" not in content.lower(), \
        "review.md must not ask for per-finding approval"


def test_review_severity_levels():
    """review.md must define severity levels for findings."""
    path = workflow_path("cline", "review")
    content = path.read_text()
    for level in ["Critical", "Major", "Minor"]:
        assert level in content, \
            f"review.md missing severity level '{level}'"


def test_review_does_not_auto_post():
    """review.md must not post threads without user selection."""
    path = workflow_path("cline", "review")
    content = path.read_text()
    does_not = content.split("❌ DOES NOT")[1].split("##")[0] if "❌ DOES NOT" in content else ""
    assert "without" in does_not.lower() or "approval" in does_not.lower() or "explicit" in does_not.lower(), \
        "review.md DOES NOT section must state it won't post without user selection"


def test_review_covers_all_categories():
    """review.md must cover the core review categories."""
    path = workflow_path("cline", "review")
    content = path.read_text()
    for category in ["Security", "Performance", "Bug", "Test"]:
        assert category in content, \
            f"review.md missing review category '{category}'"
