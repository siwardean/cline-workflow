# /morning.md — Daily Status & Planning

## Objective
Start the day with a comprehensive status check:
- Review MR threads and pipeline status
- Check SonarQube quality metrics
- Identify priorities for today

## Prerequisites
- `memory-bank/current-mr.md` configured with project_id, mr_iid, sonar_project_key

## Steps (tool-first)

### 1) Read configuration
```
read_file: memory-bank/current-mr.md
```
Extract: project_id, mr_iid, base_branch, feature_branch, sonar_project_key

**Error handling:** If file missing or fields empty, stop and ask user to configure it.

### 2) Check Git status
```
run_terminal_cmd: git status
run_terminal_cmd: git log --oneline -5
```
Show user their current branch and recent commits.

### 3) Fetch GitLab MR data (via MCP)
**List MCP tools available** to discover exact tool names, then fetch:
- MR metadata (use tool like `gitlab_get_merge_request` or similar)
- MR discussions/threads (use tool like `gitlab_get_discussions` or similar)
- Pipeline status (use tool like `gitlab_get_pipeline` or similar)

**Error handling:** If MCP fails, inform user and suggest:
```
python validate_mcp_setup.py
```

### 4) Fetch SonarQube data (via MCP)
**List MCP tools available** to discover exact tool names, then fetch:
- Quality gate status (pass/fail + conditions)
- Issues by severity (bugs, vulnerabilities, code smells)
- Coverage metrics (overall % + new code %)

**Error handling:** If SonarQube unavailable, proceed with GitLab data only and note limitation.

### 5) Analyze and prioritize
Cross-reference:
- Unresolved MR threads → tasks
- SonarQube issues → remediation work
- Pipeline failures → fixes needed

Create priority matrix:
- **High**: Quality gate blockers, security vulnerabilities, pipeline failures
- **Medium**: Bugs, unresolved reviewer threads
- **Low**: Code smells, minor improvements

### 6) Present summary
Format output as:
```
🌅 Morning Status for MR !{mr_iid}

📋 GitLab Status:
- Branch: {feature_branch}
- Pipeline: ✅ PASSING / ❌ FAILED / 🔄 RUNNING
- Last updated: {time}

💬 MR Threads ({count} unresolved):
[List each unresolved thread with file, line, reviewer, comment]

📊 SonarQube Status:
{quality_gate_emoji} Quality Gate: {status}
Coverage: {coverage}% ({diff} vs base)
Issues: {bugs} bugs, {vulns} vulnerabilities, {smells} code smells

[Detail blocking issues if any]

🎯 Today's Priorities:
1. [Highest priority item]
2. [Second priority item]
...

Next steps: [Suggested action]
```

## Output
- Comprehensive status report
- Prioritized task list
- Suggested next actions

## Success Criteria
- User has clear picture of MR health
- Priorities are actionable and ordered
- All quality signals surfaced
