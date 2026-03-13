---
name: eod
description: Update MR description and draft thread replies
---

# End of Day MR Update (Multi-MR Support)

## What This Workflow Does

**Updates selected MR(s) on GitLab and drafts replies to reviewer threads.**

### ✅ DOES:
- Lists all your active MRs
- Asks which MR(s) to update
- Fetches latest SonarQube status
- Updates GitLab MR description (fills template)
- Drafts professional replies to resolved threads
- Updates `memory-bank/handover.md` with progress

### ❌ DOES NOT:
- Does NOT post replies to GitLab (shows drafts to copy/paste)
- Does NOT resolve threads
- Does NOT merge MRs
- Does NOT write code

## Prerequisites
- `memory-bank/current-mr.md` configured with merge_requests list
- `.gitlab/merge_request_templates/default_merge_request.md` exists
- MRs already created in GitLab

## Input
- Your selection of which MR(s) to update

## Output
- Updated MR description(s) on GitLab
- Draft thread replies in chat (copy/paste ready)
- Updated `memory-bank/handover.md`

## Steps (tool-first)

### 1) Read configuration and list MRs
```
read_file: memory-bank/current-mr.md
read_file: memory-bank/story.md (if exists)
```
Extract: project_id, merge_requests list, mr_template_path, story context

**Show user all active MRs:**
```
Your active MRs:
1. !67 - feature/user-authentication: "User authentication with JWT"
2. !68 - feature/password-reset: "Password reset flow"

Which MR(s) would you like to update? (enter number, or 'all')
```

**Wait for user selection before proceeding.**

### 2) Fetch latest SonarQube status (via MCP)
**List MCP tools available**, then fetch:
- Quality gate status (PASS/FAIL + reason)
- Coverage metrics (% + diff)
- New issues introduced (bugs, vulnerabilities, code smells)
- Security hotspots

**Error handling:** If SonarQube unavailable, note this in MR update and proceed.

### 3) Check git status
```
run_terminal_cmd: git log --oneline -10
run_terminal_cmd: git diff --stat origin/{base_branch}...HEAD
```
Get recent commits and changes for handover.

### 4) Update MR description (via GitLab MCP)
**Read the MR template:**
```
read_file: .gitlab/merge_request_templates/default.md
```

**Fill in the template with:**
- Summary: from story.md or current MR description
- Proposed changes: from git log and story plan
- Risk and limitations: from SonarQube issues
- How to test: from story.md test plan
- Proof: 
  - SonarQube quality gate status
  - Coverage metrics
  - Pipeline status
  - Test results

**Update MR description** using GitLab MCP (tool like `gitlab_update_merge_request` or similar)

**Error handling:** If MCP update fails, show filled template to user for manual copy.

### 5) Draft replies to resolved threads (via GitLab MCP)
**Fetch MR discussions** (use GitLab MCP tool)

For each thread that:
- Was opened by a reviewer
- Has been addressed in recent commits
- Is not yet resolved

**Draft a reply in this format:**
```
Thanks for the feedback! I've addressed this.

Changes:
- [What was changed]
- [Where in the code]

Evidence:
- Commit: [commit sha]
- Tests: [test file or command to run]
- [Screenshot or proof if applicable]

Can you verify and resolve the thread?
```

**Present drafts to user** for review and manual posting to GitLab.

### 6) Update handover
```
read_file: memory-bank/handover.md (to see previous state)
run_terminal_cmd: git log --oneline --since="8 hours ago"
run_terminal_cmd: git rev-parse HEAD
```

**Write updated handover:**
```
write: memory-bank/handover.md
```

Format:
```markdown
# Handover (latest)
<!-- This file is automatically updated by the /eod.md workflow -->

date: {today}
branch: {feature_branch}
base: {base_branch}
last_checkpoint_commit: {sha}

## What changed today
- [List commits from today]
- [Key changes made]

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

### 7) Present summary
Show user:
```
🌆 End of Day Summary

✅ MR Description: [UPDATED / FAILED]
✅ Thread Replies: [count] drafts prepared
✅ Handover: Updated

📝 Draft Replies (copy to GitLab):
[Show each draft with thread reference]

Next: Copy the draft replies to GitLab and resolve threads!
```

## Output
- Updated MR description (following template)
- Draft thread replies (ready to post)
- Updated handover document
- Clear summary of day's progress

## Success Criteria
- MR description accurately reflects current state
- Thread replies are professional and helpful
- Handover enables easy pickup tomorrow
- User knows what to copy/paste to GitLab
