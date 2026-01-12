# Current Project Configuration
# ⚠️ UPDATE THESE VALUES FOR YOUR PROJECT ⚠️

base_branch: main

# GitLab project configuration
project_id: 123

# Merge Requests to track (add multiple MRs here!)
merge_requests:
  - mr_iid: 67
    feature_branch: feature/user-authentication
    description: "User authentication with JWT"
  
  - mr_iid: 68
    feature_branch: feature/password-reset
    description: "Password reset flow"
  
  # Add more MRs as needed:
  # - mr_iid: 69
  #   feature_branch: feature/profile-page
  #   description: "User profile page"

# SonarQube configuration
sonar_project_key: my-project

# MR template path (relative to repo root)
mr_template_path: .gitlab/merge_request_templates/default_merge_request.md

# Pre-commit hook runner (optional)
# Options: "lint-staged" | "pre-commit" | "both" | null
precommit_runner: null
