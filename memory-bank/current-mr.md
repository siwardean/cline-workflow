# Current MR Configuration
# ⚠️ UPDATE THESE VALUES FOR YOUR PROJECT ⚠️

base_branch: main
feature_branch: feature-x

# GitLab project configuration
project_id: 123
mr_iid: 1

# SonarQube configuration
sonar_project_key: my-project

# MR template path (relative to repo root)
mr_template_path: .gitlab/merge_request_templates/default.md

# Pre-commit hook runner (optional)
# Options: "lint-staged" | "pre-commit" | "both" | null
# If set, the /commit.md workflow will automatically run these hooks
precommit_runner: null
