# /morning.md — Daily Status Check (Multi-MR Support)

## What This Workflow Does

**Checks status across ALL your merge requests and provides prioritized task list.**

### ✅ DOES:
- Fetches GitLab data for ALL MRs (threads, pipeline status)
- Fetches SonarQube metrics (quality gate, coverage, issues)
- Prioritizes work based on severity
- Suggests which MR to focus on first

### ❌ DOES NOT:
- Does NOT modify any files
- Does NOT update GitLab
- Does NOT write code
- Does NOT commit anything

## Prerequisites
- `memory-bank/current-mr.md` configured with project_id, merge_requests list, sonar_project_key
- MRs already created in GitLab
- MCP servers configured

## Input
- None (reads from `memory-bank/current-mr.md`)

## Output
- Status report in chat showing all MRs
- Prioritized task list
- Suggested focus area

## Steps (tool-first)

### 1) Read configuration
```
read_file: memory-bank/current-mr.md
```
Extract: project_id, merge_requests (list with mr_iid, feature_branch, description), base_branch, sonar_project_key

**Error handling:** If file missing or fields empty, stop and ask user to configure it.

**Multi-MR handling:** Process each MR in the merge_requests list.

### 2) Check Git status
```
run_terminal_cmd: git status
run_terminal_cmd: git log --oneline -5
```
Show user their current branch and recent commits.

### 3) Fetch GitLab MR data (via MCP) - FOR EACH MR
**List MCP tools available** to discover exact tool names.

**For each MR in merge_requests list:**
- MR metadata (use tool like `gitlab_get_merge_request` with mr_iid)
- MR discussions/threads (use tool like `gitlab_get_discussions` with mr_iid)
- Pipeline status (use tool like `gitlab_get_pipeline` with mr_iid)

**Error handling:** If MCP fails for any MR, note it and continue with others. Suggest:
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

### 6) Present summary for ALL MRs
Format output as:
```
🌅 Morning Status - Project: {project_id}

📊 SonarQube Overall Status:
{quality_gate_emoji} Quality Gate: {status}
Coverage: {coverage}% ({diff} vs base)
Issues: {bugs} bugs, {vulns} vulnerabilities, {smells} code smells

═══════════════════════════════════════════════════════

📋 MR !{mr_iid_1}: {description}
Branch: {feature_branch}
Pipeline: ✅ PASSING / ❌ FAILED / 🔄 RUNNING
💬 Threads: {count} unresolved
Priority: {HIGH/MEDIUM/LOW based on status}

[If HIGH priority: list blocking issues]

───────────────────────────────────────────────────────

📋 MR !{mr_iid_2}: {description}
Branch: {feature_branch}
Pipeline: ✅ PASSING / ❌ FAILED / 🔄 RUNNING
💬 Threads: {count} unresolved
Priority: {HIGH/MEDIUM/LOW based on status}

[If HIGH priority: list blocking issues]

═══════════════════════════════════════════════════════

🎯 Overall Priorities:
1. [Highest priority across all MRs]
2. [Second priority]
3. [Third priority]

💡 Suggested Focus: Start with MR !{mr_iid} ({reason})
```

## Output
- Comprehensive status report
- Prioritized task list
- Suggested next actions

## Success Criteria
- User has clear picture of MR health
- Priorities are actionable and ordered
- All quality signals surfaced
