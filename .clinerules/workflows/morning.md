---
name: morning
description: Daily ritual — wraps up yesterday then starts your day with a full status check
---

# Daily Ritual (Wrap Up Yesterday → Start Today)

## What This Workflow Does

**Runs at the start of your day. Closes out yesterday first, then gives you a fresh status for today.**

### ✅ DOES:
1. Updates all active MR descriptions on GitLab with current state
2. Drafts professional replies to resolved reviewer threads
3. Writes `memory-bank/handover.md`
4. Fetches live GitLab and SonarQube status across all MRs
5. Delivers a prioritised task list for the day

### ❌ DOES NOT:
- Does NOT post replies to GitLab (shows drafts to copy/paste)
- Does NOT resolve threads or merge MRs
- Does NOT write production code
- Does NOT commit code changes

## Prerequisites
- `memory-bank/current-mr.md` configured with `project_id`, `merge_requests`, `base_branch`, `sonar_project_key`
- `.gitlab/merge_request_templates/default.md` exists in the project
- MRs already created in GitLab
- MCP servers configured

---

## Steps

### 1) Read configuration
```
read_file: memory-bank/current-mr.md
read_file: memory-bank/story.md (if exists)
```
Extract: `project_id`, `merge_requests` (list with `mr_iid`, `feature_branch`, `description`), `base_branch`, `sonar_project_key`.

**Error handling:** If file missing or required fields empty, stop and ask the user to configure it.

---

## Phase 1 — Wrap Up Yesterday

### 2) Check git status
```
run_terminal_cmd: git log --oneline -10
run_terminal_cmd: git diff --stat origin/{base_branch}...HEAD
```

### 3) Fetch SonarQube status (via MCP)
**List MCP tools available**, then fetch:
- Quality gate status (PASS/FAIL + reason)
- Coverage metrics (% + diff)
- New issues introduced (bugs, vulnerabilities, code smells)
- Security hotspots

**Error handling:** If SonarQube unavailable, note it in MR updates and proceed.

### 4) Update MR descriptions (via GitLab MCP) — all active MRs
Read the MR template:
```
read_file: .gitlab/merge_request_templates/default.md
```

For each MR in `merge_requests`, fill in the template with:
- Summary: from `story.md` or current MR description
- Proposed changes: from git log and story plan
- Risk and limitations: from SonarQube issues
- How to test: from `story.md` test plan
- Proof: SonarQube quality gate, coverage, pipeline status, test results

Update each MR description using GitLab MCP (`gitlab_update_merge_request` or equivalent).

**Error handling:** If MCP update fails for any MR, show the filled template for manual copy and continue with the next.

### 5) Draft replies to resolved threads (via GitLab MCP)
For each MR, fetch discussions. For each thread that was opened by a reviewer, addressed in recent commits, and not yet resolved, draft:
```
Thanks for the feedback! I've addressed this.

Changes:
- [What was changed]
- [Where in the code]

Evidence:
- Commit: [commit sha]
- Tests: [test file or command to run]

Can you verify and resolve the thread?
```

Collect all drafts — they will be shown at the end.

### 6) Write handover
```
run_terminal_cmd: git log --oneline --since="24 hours ago"
run_terminal_cmd: git rev-parse HEAD
```

Write `memory-bank/handover.md`:
```markdown
# Handover (latest)
<!-- Updated by morning.md -->

date: {today}
branch: {feature_branch}
base: {base_branch}
last_checkpoint_commit: {sha}

## What changed recently
- [Commits from last 24h]

## Current state
✅ Implemented: [Completed tasks]
🔄 In progress: [Partial tasks]
📋 Not started: [Remaining tasks]

## Tests / CI
- Tests: [Status]
- Pipeline: [Status]
- SonarQube: [Quality gate status]
- Coverage: [%]

## Risks / blockers
[Any issues blocking progress]

## Suggested next steps
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## Open MR threads (summary)
[Count and brief summary of unresolved threads]
```

---

## Phase 2 — Start Today

### 7) Fetch fresh GitLab MR data (via MCP) — for each MR
For each MR in `merge_requests`:
- MR metadata (`gitlab_get_merge_request` with `mr_iid`)
- MR discussions/threads (`gitlab_get_discussions` with `mr_iid`)
- Pipeline status (`gitlab_get_pipeline` with `mr_iid`)

**Error handling:** If MCP fails for any MR, note it and continue with others.

### 8) Fetch fresh SonarQube data (via MCP)
- Quality gate status (pass/fail + conditions)
- Issues by severity (bugs, vulnerabilities, code smells)
- Coverage metrics (overall % + new code %)

### 9) Analyse and prioritise
Cross-reference:
- Unresolved MR threads → tasks
- SonarQube issues → remediation work
- Pipeline failures → fixes needed

Priority matrix:
- **High**: Quality gate blockers, security vulnerabilities, pipeline failures
- **Medium**: Bugs, unresolved reviewer threads
- **Low**: Code smells, minor improvements

### 10) Present full daily report
```
🌅 Good morning — Project: {project_id}

━━━ Yesterday's wrap-up ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ MR Descriptions updated: {count}
✅ Thread reply drafts:     {count} (see below)
✅ Handover:                written

━━━ Today's status ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SonarQube:
{quality_gate_emoji} Quality Gate: {status}
Coverage: {coverage}% ({diff} vs base)
Issues: {bugs} bugs, {vulns} vulnerabilities, {smells} code smells

═══════════════════════════════════════════════════════

📋 MR !{mr_iid}: {description}
Branch: {feature_branch}
Pipeline: ✅ PASSING / ❌ FAILED / 🔄 RUNNING
💬 Threads: {count} unresolved
Priority: HIGH / MEDIUM / LOW

[Repeat for each MR]

═══════════════════════════════════════════════════════

🎯 Today's Priorities:
1. [Highest priority]
2. [Second priority]
3. [Third priority]

💡 Start with: MR !{mr_iid} ({reason})

━━━ Thread reply drafts (copy to GitLab) ━━━━━━━━━━━━

[Each draft with MR reference and thread context]
```

---

## Success Criteria
- MR descriptions are up to date before the day starts
- Thread reply drafts are ready to post
- Handover reflects current state
- Developer has a clear, prioritised picture of what to work on
