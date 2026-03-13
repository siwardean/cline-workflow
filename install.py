#!/usr/bin/env python3
"""
AI-Assisted Workflows — Interactive Installer

Sets up workflows for your AI coding assistant and optionally configures
an existing project with memory-bank/current-mr.md.

Usage:
    python install.py
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()

# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------

def header(text):
    width = 60
    print(f"\n{'─' * width}")
    print(f"  {text}")
    print(f"{'─' * width}")


def step(n, text):
    print(f"\n[{n}] {text}")


def ok(text):
    print(f"  ✅ {text}")


def warn(text):
    print(f"  ⚠️  {text}")


def err(text):
    print(f"  ❌ {text}")


def ask(prompt, default=""):
    hint = f" [{default}]" if default else ""
    try:
        value = input(f"  {prompt}{hint}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    return value or default


def ask_choice(prompt, options, default=0):
    """Present a numbered menu and return the chosen index."""
    print(f"\n  {prompt}")
    for i, opt in enumerate(options):
        marker = " (default)" if i == default else ""
        print(f"    {i + 1}) {opt}{marker}")
    while True:
        try:
            raw = input(f"  Enter number [1–{len(options)}] or press Enter for default: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)
        if not raw:
            return default
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return int(raw) - 1
        print(f"  Please enter a number between 1 and {len(options)}")


def ask_multi(prompt, options):
    """Present a numbered menu and return list of chosen indices (space-separated)."""
    print(f"\n  {prompt}")
    for i, opt in enumerate(options):
        print(f"    {i + 1}) {opt}")
    print("  Enter numbers separated by spaces (e.g. 1 3), or 'a' for all:")
    while True:
        try:
            raw = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)
        if raw == "a":
            return list(range(len(options)))
        parts = raw.split()
        if all(p.isdigit() and 1 <= int(p) <= len(options) for p in parts) and parts:
            return [int(p) - 1 for p in parts]
        print(f"  Please enter valid numbers between 1 and {len(options)}")


def confirm(prompt, default=True):
    hint = "Y/n" if default else "y/N"
    try:
        raw = input(f"  {prompt} [{hint}]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    if not raw:
        return default
    return raw in ("y", "yes")


# ---------------------------------------------------------------------------
# MCP config paths per tool
# ---------------------------------------------------------------------------

def cline_mcp_path():
    """Best-effort Cline MCP settings path (varies by OS and VS Code flavor)."""
    candidates = [
        # Linux — VS Code
        Path.home() / ".config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json",
        # Linux — VS Code Insiders
        Path.home() / ".config/Code - Insiders/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json",
        # macOS — VS Code
        Path.home() / "Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json",
        # macOS — VS Code Insiders
        Path.home() / "Library/Application Support/Code - Insiders/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json",
    ]
    for p in candidates:
        if p.exists():
            return p
    # Return the Linux default as fallback (will be created)
    return candidates[0]


def kilocode_mcp_path():
    candidates = [
        Path.home() / ".config/Code/User/globalStorage/kilocode.kilo-code/settings/cline_mcp_settings.json",
        Path.home() / "Library/Application Support/Code/User/globalStorage/kilocode.kilo-code/settings/cline_mcp_settings.json",
    ]
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]


TOOLS = {
    "Claude Code": {
        "workflow_src":   HERE / ".claude",
        "workflow_dest":  None,          # per-project; handled separately
        "rules_src":      HERE / "CLAUDE.md",
        "global_rules":   Path.home() / ".claude" / "CLAUDE.md",
        "mcp_path":       Path.home() / ".claude" / "settings.json",
        "mcp_key":        "mcpServers",
        "install_hint":   "Copy to project root + .claude/commands/",
    },
    "Cline": {
        "workflow_src":   HERE / ".clinerules" / "workflows",
        "rules_src":      HERE / ".clinerules" / "rules.md",
        "global_workflow": Path.home() / "Documents" / "Cline" / "Workflows",
        "global_rules":   Path.home() / "Documents" / "Cline" / "Rules" / "rules.md",
        "mcp_path":       None,          # resolved at runtime
        "mcp_key":        "mcpServers",
    },
    "Kilo Code": {
        "workflow_src":   HERE / ".kilocoderules" / "workflows",
        "rules_src":      HERE / ".kilocoderules" / "rules.md",
        "global_workflow": Path.home() / "Documents" / "KiloCode" / "Workflows",
        "global_rules":   Path.home() / "Documents" / "KiloCode" / "Rules" / "rules.md",
        "mcp_path":       None,
        "mcp_key":        "mcpServers",
    },
    "Cursor": {
        "workflow_src":   HERE / ".cursor",
        "workflow_dest":  None,          # per-project
        "global_rules":   None,
        "mcp_path":       None,          # per-project .cursor/mcp.json
        "mcp_key":        "mcpServers",
        "install_hint":   "Copy .cursor/ to each project root",
    },
    "OpenCode": {
        "workflow_src":   HERE / ".clinerules",
        "workflow_dest":  None,          # per-project
        "mcp_path":       Path.home() / ".config" / "opencode" / "config.json",
        "mcp_key":        "mcpServers",
        "install_hint":   "Copy .clinerules/ to each project root",
    },
}


# ---------------------------------------------------------------------------
# Package installation
# ---------------------------------------------------------------------------

def install_packages():
    step(1, "Installing MCP packages")

    uv = shutil.which("uv")
    pip = shutil.which("pip3") or shutil.which("pip")

    if uv:
        cmd = [uv, "pip", "install", "python-gitlab-mcp", "sonar-mcp"]
        runner = "uv"
    elif pip:
        cmd = [pip, "install", "python-gitlab-mcp", "sonar-mcp"]
        runner = "pip"
    else:
        warn("Neither uv nor pip found.")
        warn("Install uv first: pip install uv")
        warn("Then run: uv pip install python-gitlab-mcp sonar-mcp")
        return False

    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        ok(f"Packages installed via {runner}")
        return True
    else:
        err("Package installation failed:")
        print(result.stderr[:500])
        return False


# ---------------------------------------------------------------------------
# Workflow file installation
# ---------------------------------------------------------------------------

def install_cline_or_kilocode(tool_name, tool):
    """Install Cline or Kilo Code workflows globally."""
    wf_dest = tool["global_workflow"]
    rules_dest = tool["global_rules"]

    wf_dest.mkdir(parents=True, exist_ok=True)
    rules_dest.parent.mkdir(parents=True, exist_ok=True)

    # Copy workflow files
    for src in tool["workflow_src"].glob("*.md"):
        shutil.copy2(src, wf_dest / src.name)
    ok(f"{tool_name} workflows → {wf_dest}")

    # Copy rules
    shutil.copy2(tool["rules_src"], rules_dest)
    ok(f"{tool_name} rules → {rules_dest}")


def install_claude_code(project_dir: Path):
    """Install Claude Code CLAUDE.md and .claude/commands/ into a project."""
    dest_claude = project_dir / ".claude"
    dest_commands = dest_claude / "commands"
    dest_commands.mkdir(parents=True, exist_ok=True)

    # Copy .claude/commands/
    src_commands = HERE / ".claude" / "commands"
    for src in src_commands.glob("*.md"):
        shutil.copy2(src, dest_commands / src.name)
    ok(f"Claude Code commands → {dest_commands}")

    # CLAUDE.md — append to existing or create fresh
    dest_claude_md = project_dir / "CLAUDE.md"
    if dest_claude_md.exists():
        if confirm("CLAUDE.md already exists in project. Append rules to it?", default=True):
            existing = dest_claude_md.read_text()
            addition = (HERE / "CLAUDE.md").read_text()
            if addition.strip() not in existing:
                dest_claude_md.write_text(existing.rstrip() + "\n\n" + addition)
                ok(f"Appended rules to {dest_claude_md}")
            else:
                ok("Rules already present in CLAUDE.md — skipped")
    else:
        shutil.copy2(HERE / "CLAUDE.md", dest_claude_md)
        ok(f"CLAUDE.md → {dest_claude_md}")

    # Offer global rules too
    global_claude_md = Path.home() / ".claude" / "CLAUDE.md"
    if confirm(f"Also append rules to global {global_claude_md}?", default=False):
        global_claude_md.parent.mkdir(parents=True, exist_ok=True)
        addition = (HERE / "CLAUDE.md").read_text()
        if global_claude_md.exists():
            existing = global_claude_md.read_text()
            if addition.strip() not in existing:
                global_claude_md.write_text(existing.rstrip() + "\n\n" + addition)
                ok(f"Appended to global {global_claude_md}")
        else:
            shutil.copy2(HERE / "CLAUDE.md", global_claude_md)
            ok(f"Created global {global_claude_md}")


def install_cursor(project_dir: Path):
    dest = project_dir / ".cursor"
    if dest.exists():
        if not confirm(f".cursor/ already exists in project. Overwrite?", default=False):
            warn("Skipped Cursor install")
            return
    shutil.copytree(HERE / ".cursor", dest, dirs_exist_ok=True)
    ok(f"Cursor rules → {dest}")


def install_opencode(project_dir: Path):
    dest = project_dir / ".clinerules"
    if dest.exists():
        if not confirm(f".clinerules/ already exists in project. Overwrite?", default=False):
            warn("Skipped OpenCode install")
            return
    shutil.copytree(HERE / ".clinerules", dest, dirs_exist_ok=True)
    ok(f"OpenCode rules → {dest}")


def install_workflows(selected_tools, project_dir):
    step(2, "Installing workflow files")

    for tool_name in selected_tools:
        print(f"\n  → {tool_name}")
        if tool_name in ("Cline", "Kilo Code"):
            install_cline_or_kilocode(tool_name, TOOLS[tool_name])
        elif tool_name == "Claude Code":
            install_claude_code(project_dir)
        elif tool_name == "Cursor":
            install_cursor(project_dir)
        elif tool_name == "OpenCode":
            install_opencode(project_dir)


# ---------------------------------------------------------------------------
# MCP configuration
# ---------------------------------------------------------------------------

def collect_mcp_credentials():
    step(3, "MCP server credentials")
    print("  These will be written into your tool's MCP config file.")
    print("  Leave blank to skip a service.\n")

    gitlab_url   = ask("GitLab URL", "https://gitlab.com")
    gitlab_token = ask("GitLab personal access token (scope: api)")
    gitlab_ids   = ask("GitLab allowed project IDs (comma-separated, e.g. 12345,67890)")

    sonar_url    = ask("SonarQube URL (leave blank to skip)")
    sonar_token  = ask("SonarQube token") if sonar_url else ""

    return {
        "gitlab": {
            "url": gitlab_url,
            "token": gitlab_token,
            "project_ids": gitlab_ids,
        },
        "sonar": {
            "url": sonar_url,
            "token": sonar_token,
        },
    }


def build_mcp_block(creds):
    block = {}
    if creds["gitlab"]["token"]:
        block["gitlab"] = {
            "command": "python-gitlab-mcp",
            "args": [],
            "env": {
                "GITLAB_URL": creds["gitlab"]["url"],
                "GITLAB_TOKEN": creds["gitlab"]["token"],
                "GITLAB_ALLOWED_PROJECT_IDS": creds["gitlab"]["project_ids"],
            },
        }
    if creds["sonar"]["token"]:
        block["sonarqube"] = {
            "command": "sonar-mcp",
            "args": [],
            "env": {
                "SONAR_URL": creds["sonar"]["url"],
                "SONAR_TOKEN": creds["sonar"]["token"],
            },
        }
    return block


def write_mcp_config(config_path: Path, mcp_key: str, mcp_block: dict):
    """Merge mcp_block into existing config file under mcp_key."""
    config_path.parent.mkdir(parents=True, exist_ok=True)

    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
        except json.JSONDecodeError:
            warn(f"Could not parse {config_path} — skipping automatic config write")
            return False
    else:
        config = {}

    # Backup
    backup = config_path.with_suffix(".json.bak")
    if config_path.exists():
        shutil.copy2(config_path, backup)

    existing_servers = config.get(mcp_key, {})
    existing_servers.update(mcp_block)
    config[mcp_key] = existing_servers

    config_path.write_text(json.dumps(config, indent=2) + "\n")
    ok(f"MCP config written → {config_path}")
    if backup.exists():
        ok(f"Backup saved → {backup}")
    return True


def configure_mcp(selected_tools, creds, project_dir):
    mcp_block = build_mcp_block(creds)
    if not mcp_block:
        warn("No MCP credentials provided — skipping MCP config")
        return

    for tool_name in selected_tools:
        if tool_name == "Claude Code":
            config_path = Path.home() / ".claude" / "settings.json"
            write_mcp_config(config_path, "mcpServers", mcp_block)

        elif tool_name == "Cline":
            config_path = cline_mcp_path()
            if not config_path.exists():
                warn(f"Cline MCP config not found at {config_path}")
                warn("Open VS Code → Cline → MCP Servers → Edit JSON and add:")
                _print_mcp_snippet(mcp_block)
            else:
                write_mcp_config(config_path, "mcpServers", mcp_block)

        elif tool_name == "Kilo Code":
            config_path = kilocode_mcp_path()
            if not config_path.exists():
                warn(f"Kilo Code MCP config not found at {config_path}")
                warn("Open VS Code → Kilo Code → MCP Servers → Edit JSON and add:")
                _print_mcp_snippet(mcp_block)
            else:
                write_mcp_config(config_path, "mcpServers", mcp_block)

        elif tool_name == "Cursor":
            config_path = project_dir / ".cursor" / "mcp.json"
            write_mcp_config(config_path, "mcpServers", mcp_block)

        elif tool_name == "OpenCode":
            config_path = Path.home() / ".config" / "opencode" / "config.json"
            write_mcp_config(config_path, "mcpServers", mcp_block)


def _print_mcp_snippet(mcp_block):
    print()
    print(json.dumps({"mcpServers": mcp_block}, indent=2))
    print()


# ---------------------------------------------------------------------------
# Project memory-bank setup
# ---------------------------------------------------------------------------

def setup_project(project_dir: Path, creds):
    step(4, f"Setting up project at {project_dir}")

    mb = project_dir / "memory-bank"
    mb.mkdir(exist_ok=True)

    target = mb / "current-mr.md"
    if target.exists():
        if not confirm("memory-bank/current-mr.md already exists. Overwrite?", default=False):
            warn("Skipped — update it manually if needed")
            return

    project_id  = ask("GitLab project ID", "12345")
    sonar_key   = ask("SonarQube project key", project_dir.name)
    base_branch = ask("Base branch", "main")
    precommit   = ask("Pre-commit runner (lint-staged / pre-commit / both / none)", "none")
    if precommit.lower() in ("none", ""):
        precommit = "null"

    content = f"""\
# Current Project Configuration
# Generated by install.py — update merge_requests list as you create MRs

base_branch: {base_branch}

# GitLab project configuration
project_id: {project_id}

# Merge Requests to track
merge_requests:
  # Add your MRs here after running start.md:
  # - mr_iid: 1
  #   feature_branch: feature/example_feature
  #   description: "Short description"

# SonarQube configuration
sonar_project_key: {sonar_key}

# MR template path (relative to repo root)
mr_template_path: .gitlab/merge_request_templates/default_merge_request.md

# Pre-commit hook runner: lint-staged | pre-commit | both | null
precommit_runner: {precommit}
"""
    target.write_text(content)
    ok(f"Created {target}")

    # Offer to create a .gitignore entry for memory-bank generated files
    gitignore = project_dir / ".gitignore"
    entry = "memory-bank/handover.md\nmemory-bank/story.md\nmemory-bank/retro.md\n"
    if gitignore.exists():
        existing = gitignore.read_text()
        if "memory-bank/handover.md" not in existing:
            if confirm("Add memory-bank AI state files to .gitignore?", default=True):
                gitignore.write_text(existing.rstrip() + "\n\n# AI workflow state (generated)\n" + entry)
                ok(".gitignore updated")
    else:
        if confirm(f"Create .gitignore with memory-bank entries?", default=True):
            gitignore.write_text("# AI workflow state (generated)\n" + entry)
            ok(".gitignore created")


# ---------------------------------------------------------------------------
# Final validation
# ---------------------------------------------------------------------------

def run_validation():
    step(5, "Running setup validation")
    validate_script = HERE / "validate_mcp_setup.py"
    if validate_script.exists():
        subprocess.run([sys.executable, str(validate_script)])
    else:
        warn("validate_mcp_setup.py not found — skipping")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("\n" + "=" * 60)
    print("  AI-Assisted Workflows — Installer")
    print("=" * 60)
    print("\nThis script will:")
    print("  1. Install MCP packages (python-gitlab-mcp, sonar-mcp)")
    print("  2. Copy workflow files to your AI tool's location")
    print("  3. Configure MCP servers with your credentials")
    print("  4. Set up memory-bank/current-mr.md in your project")
    print("  5. Validate the installation")
    print("\nPress Ctrl+C at any time to exit.\n")

    # Which tools?
    header("Which AI tools do you use?")
    tool_names = list(TOOLS.keys())
    chosen_indices = ask_multi("Select your tools", tool_names)
    selected_tools = [tool_names[i] for i in chosen_indices]
    print(f"\n  Selected: {', '.join(selected_tools)}")

    # Project directory (needed for per-project installs and memory-bank setup)
    needs_project_dir = any(t in selected_tools for t in ("Claude Code", "Cursor", "OpenCode"))
    project_dir = None

    header("Project setup")
    raw = ask("Path to your GitLab project (leave blank to use current directory)", str(Path.cwd()))
    project_dir = Path(raw).expanduser().resolve()
    if not project_dir.exists():
        err(f"Directory not found: {project_dir}")
        sys.exit(1)
    ok(f"Project: {project_dir}")

    # Step 1: packages
    header("Step 1 — MCP Packages")
    if not install_packages():
        if not confirm("Continue anyway?", default=False):
            sys.exit(1)

    # Step 2: workflows
    header("Step 2 — Workflow Files")
    install_workflows(selected_tools, project_dir)

    # Step 3: MCP credentials
    header("Step 3 — MCP Configuration")
    if confirm("Configure MCP server credentials now?", default=True):
        creds = collect_mcp_credentials()
        configure_mcp(selected_tools, creds, project_dir)
    else:
        warn("Skipped — add credentials manually to your tool's MCP settings")
        creds = {"gitlab": {}, "sonar": {}}

    # Step 4: project setup
    header("Step 4 — Project memory-bank")
    if confirm(f"Set up memory-bank/current-mr.md in {project_dir}?", default=True):
        setup_project(project_dir, creds)

    # Step 5: validate
    header("Step 5 — Validation")
    if confirm("Run validation check?", default=True):
        run_validation()

    # Done
    header("Done!")
    print("\n  Next steps:")
    if "Claude Code" in selected_tools:
        print("  • Claude Code: run /morning in your project to verify")
    if any(t in selected_tools for t in ("Cline", "Kilo Code", "OpenCode")):
        print('  • Cline/Kilo Code/OpenCode: say "Run the morning.md workflow"')
    if "Cursor" in selected_tools:
        print("  • Cursor: open your project and say 'Run morning.md'")
    print("  • Update memory-bank/current-mr.md when you create your first MR")
    print()


if __name__ == "__main__":
    main()
