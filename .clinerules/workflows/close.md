# /close.md — Post-Merge Retrospective

## What This Workflow Does

**Analyzes completed feature and writes lessons learned.**

### ✅ DOES:
- Fetches merged MR data from GitLab (dates, discussions)
- Compares delivery vs original plan
- Evaluates acceptance criteria compliance
- Calculates estimate variance (planned vs actual)
- Identifies lessons learned
- Writes retrospective to `memory-bank/retro.md`

### ❌ DOES NOT:
- Does NOT merge the MR (you merge in GitLab UI)
- Does NOT modify code
- Does NOT update GitLab
- Does NOT delete branches

## Prerequisites
- MR already merged in GitLab
- `memory-bank/story.md` exists (from start.md workflow)
- `memory-bank/current-mr.md` configured

## Input
- None (reads merged MR from GitLab)

## Output
- `memory-bank/retro.md` with detailed retrospective and lessons learned

## Steps (tool-first)

### 1) Read baseline and configuration
```
read_file: memory-bank/story.md
read_file: memory-bank/current-mr.md
```

Extract:
- Original plan and ACs
- Estimate (man-days)
- Start date
- Project details for MCP

**Error handling:** If story.md missing, ask user for story details or skip detailed comparison.

### 2) Fetch MR data (via GitLab MCP)
**List MCP tools available**, then:

**Fetch MR metadata:**
```
Use tool like: gitlab_get_merge_request
```
Extract: created_at, merged_at, state
**Confirm state = "merged"** - if not, warn user and ask if they want to continue.

**Fetch MR discussions:**
```
Use tool like: gitlab_get_discussions
```
Analyze:
- Total thread count
- Themes (security, performance, style, etc.)
- Quality of remediation
- Reviewer engagement

**Fetch final pipeline:**
```
Use tool like: gitlab_get_pipeline (latest)
```
Get final test/quality results.

**Error handling:** If MCP unavailable, skip GitLab analysis and note in retro.

### 3) Analyze repository changes
**Update base branch:**
```
run_terminal_cmd: git fetch origin
run_terminal_cmd: git checkout {base_branch}
run_terminal_cmd: git pull origin {base_branch}
```

**Find merge commit:**
```
run_terminal_cmd: git log --merges --grep="Merge.*{feature_branch}" --oneline -5
```

**Identify what changed:**
```
run_terminal_cmd: git diff --name-only {base_branch}~1 {base_branch}
run_terminal_cmd: git log --oneline {base_branch}~20..{base_branch} --no-merges
```

### 4) Evaluate delivery

**For each Acceptance Criterion:**
```
AC{N}: {criteria text}
✅ Met / ⚠️ Partially met / ❌ Not met

Evidence:
- Implementation: {file}:{function/component}
- Tests: {test file}:{test name}
- Commit: {sha}
- MR discussion: {thread reference if applicable}

Notes: {why partial or not met}
```

**Plan vs Reality:**
Compare story.md tasks against:
```
run_terminal_cmd: git log --oneline {base_branch}~20..{base_branch} --no-merges
```

- Completed as planned: {count}/{total}
- Skipped: {list + reasons}
- Unplanned work: {list + why needed}

**Time Analysis:**
```
Estimate: {man-days from story.md}
Actual: {calendar days from created_at to merged_at}
Variance: {difference} ({percentage}%)

Factors:
- {what caused variance}
```

**Quality Review:**
- Tests added: {count}
- Coverage: {final %} (diff: {+/-})
- SonarQube final status: {gate status}
- Reviewer feedback: {summary of themes}

**Lessons Learned:**
What went well:
- {positive findings}

What could improve:
- {areas for improvement}

Root causes:
- {why variance or issues occurred}

### 5) Generate recommendations

**For next feature:**
- Process improvements: {actionable items}
- Technical improvements: {actionable items}
- Estimation improvements: {how to estimate better}

### 6) Write retrospective
```
write: memory-bank/retro.md
```

Use the template structure from retro.md, filling with analysis.

## Output
- AC compliance summary
- Estimate vs actual
- Feedback (what went well / improve)
- Concrete improvements for next feature
