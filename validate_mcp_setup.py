#!/usr/bin/env python3
"""
MCP Setup Validation Script

This script validates that GitLab and SonarQube MCP servers are properly
configured and accessible. Run this before using the Cline workflows.

Usage:
    python validate_mcp_setup.py
"""

import sys
import os
from pathlib import Path


def print_header(text):
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print('=' * 60)


def check_file_exists(filepath, description):
    """Check if a required file exists."""
    path = Path(filepath)
    if path.exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {filepath}")
        return False


def check_env_var(var_name, description):
    """Check if an environment variable is set."""
    value = os.getenv(var_name)
    if value:
        # Mask sensitive values
        masked = value[:4] + '...' + value[-4:] if len(value) > 8 else '***'
        print(f"✅ {description}: {masked}")
        return True
    else:
        print(f"❌ {description} NOT SET: {var_name}")
        return False


def validate_memory_bank():
    """Validate memory-bank configuration."""
    print_header("Memory Bank Configuration")
    
    all_good = True
    
    # Check current-mr.md
    mr_config = Path("memory-bank/current-mr.md")
    if mr_config.exists():
        print("✅ memory-bank/current-mr.md exists")
        
        content = mr_config.read_text()
        
        # Check for placeholder values
        if "project_id: 123" in content or "feature-x" in content:
            print("⚠️  WARNING: memory-bank/current-mr.md contains placeholder values")
            print("   Update project_id, mr_iid, and branch names before running workflows")
            all_good = False
        else:
            print("✅ Configuration appears to be customized")
    else:
        print("❌ memory-bank/current-mr.md NOT FOUND")
        all_good = False
    
    return all_good


def validate_gitlab_mcp():
    """Validate GitLab MCP configuration."""
    print_header("GitLab MCP Configuration")
    
    all_good = True
    
    print("\nNote: These environment variables should be configured in Cline → MCP Servers")
    print("This script cannot read Cline's MCP configuration directly.\n")
    
    # Check for environment variables (may not be set if running outside Cline)
    env_checks = [
        ("GITLAB_URL", "GitLab URL"),
        ("GITLAB_TOKEN", "GitLab Token"),
        ("GITLAB_ALLOWED_PROJECT_IDS", "Allowed Project IDs"),
    ]
    
    any_set = False
    for var, desc in env_checks:
        if check_env_var(var, desc):
            any_set = True
        else:
            all_good = False
    
    if not any_set:
        print("\n⚠️  No GitLab environment variables detected in current shell.")
        print("   This is expected if running outside of Cline.")
        print("   Ensure these are configured in: Cline → MCP Servers → GitLab MCP")
    
    return all_good


def validate_sonar_mcp():
    """Validate SonarQube MCP configuration."""
    print_header("SonarQube MCP Configuration")
    
    all_good = True
    
    print("\nNote: These environment variables should be configured in Cline → MCP Servers")
    print("This script cannot read Cline's MCP configuration directly.\n")
    
    env_checks = [
        ("SONAR_URL", "SonarQube URL"),
        ("SONAR_TOKEN", "SonarQube Token"),
    ]
    
    any_set = False
    for var, desc in env_checks:
        if check_env_var(var, desc):
            any_set = True
        else:
            all_good = False
    
    if not any_set:
        print("\n⚠️  No SonarQube environment variables detected in current shell.")
        print("   This is expected if running outside of Cline.")
        print("   Ensure these are configured in: Cline → MCP Servers → SonarQube MCP")
    
    return all_good


def validate_project_structure():
    """Validate project file structure."""
    print_header("Project Structure")
    
    all_good = True
    
    required_files = [
        (".clinerules/rules.md", "Cline rules"),
        (".clinerules/workflows/start.md", "Start workflow"),
        (".clinerules/workflows/morning.md", "Morning workflow"),
        (".clinerules/workflows/eod.md", "EOD workflow"),
        (".clinerules/workflows/commit.md", "Commit workflow"),
        (".clinerules/workflows/close.md", "Close workflow"),
        ("memory-bank/current-mr.md", "MR configuration"),
        ("memory-bank/handover.md", "Handover template"),
        ("memory-bank/story.md", "Story template"),
        ("memory-bank/retro.md", "Retro template"),
        (".gitlab/merge_request_templates/default.md", "MR template"),
        (".gitignore", "Git ignore file"),
    ]
    
    for filepath, desc in required_files:
        if not check_file_exists(filepath, desc):
            all_good = False
    
    return all_good


def validate_mcp_packages():
    """Check if MCP packages are installed."""
    print_header("MCP Package Installation")
    
    all_good = True
    
    packages = ["gitlab-mcp", "sonar-mcp"]
    
    for package in packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            print(f"   Install with: uv pip install {package}")
            all_good = False
    
    return all_good


def main():
    """Run all validation checks."""
    print("\n" + "=" * 60)
    print("  Cline GitLab Feature Workflow Kit - MCP Validation")
    print("=" * 60)
    
    checks = [
        ("Project Structure", validate_project_structure),
        ("Memory Bank", validate_memory_bank),
        ("MCP Packages", validate_mcp_packages),
        ("GitLab MCP", validate_gitlab_mcp),
        ("SonarQube MCP", validate_sonar_mcp),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ Error during {name} validation: {e}")
            results[name] = False
    
    # Summary
    print_header("Validation Summary")
    
    all_passed = all(results.values())
    
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✅ All checks passed! You're ready to use the workflows.")
        return 0
    else:
        print("❌ Some checks failed. Please review the errors above.")
        print("\nNext steps:")
        print("1. Update memory-bank/current-mr.md with your project details")
        print("2. Configure MCP servers in Cline → MCP Servers")
        print("3. Install missing packages: uv pip install gitlab-mcp sonar-mcp")
        print("4. Run this script again to verify")
        return 1


if __name__ == "__main__":
    sys.exit(main())

