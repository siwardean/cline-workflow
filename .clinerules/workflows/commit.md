# /commit.md — Commit Helper (Conventional Commits + Hooks)

## What This Workflow Does

**Helps you make clean, professional commits with proper messages.**

### ✅ DOES:
- Shows `git status` and `git diff` of your changes
- Stages changes (with your confirmation)
- Runs pre-commit hooks (lint-staged, pre-commit)
- Auto-fixes linting errors when possible
- Proposes Angular Conventional Commit message (type, scope, subject)
- Commits **only after you explicitly approve**
- Pushes to remote branch

### ❌ DOES NOT:
- Does NOT write code
- Does NOT create branches
- Does NOT merge branches
- Does NOT commit without your approval
- Does NOT create MRs

## Prerequisites
- Git repository initialized
- Changes made to files (either staged or unstaged)
- Remote branch exists (or will create on first push)

## Input
- Your code changes (modified files)
- Your approval to commit

## Output
- Committed changes with proper conventional commit message
- Pushed to remote branch

## Steps
1) Facts:
   - `run_terminal_cmd`: `git status`
   - `run_terminal_cmd`: `git diff`
   - `run_terminal_cmd`: `git diff --staged`

2) If nothing staged:
   - propose staging approach:
     - `git add <files>` OR `git add -p`
   - stop for user confirmation before staging

3) Once staged:
   - `run_terminal_cmd`: `git diff --staged --stat`
   - `run_terminal_cmd`: `git diff --staged`

4) Run pre-commit hooks:

**Read configuration:**
```
read_file: memory-bank/current-mr.md
```
Check `precommit_runner` field.

**Run appropriate hooks:**

If `precommit_runner: "lint-staged"`:
```
run_terminal_cmd: npx lint-staged
```

If `precommit_runner: "pre-commit"`:
```
run_terminal_cmd: git diff --staged --name-only
run_terminal_cmd: pre-commit run --files {staged files}
```

If `precommit_runner: "both"`:
```
run_terminal_cmd: npx lint-staged
run_terminal_cmd: pre-commit run --files {staged files}
```

If `precommit_runner: null` or not set:
Detect by checking for config files:
```
list_dir: . (look for .pre-commit-config.yaml, package.json)
```
Propose appropriate command or skip hooks.

**Error handling:** If hooks not installed, inform user and skip (don't fail).

5) If hooks fail:

**Parse failures:**
- Extract file paths and error messages
- Categorize: lint errors, format errors, test failures, type errors

**Attempt auto-fix** (for fixable issues only):
- ESLint: `run_terminal_cmd: npx eslint --fix {files}`
- Prettier: `run_terminal_cmd: npx prettier --write {files}`
- Black (Python): `run_terminal_cmd: black {files}`

For non-fixable issues:
- Show errors to user
- Ask: "Should I fix these manually?" 
- If yes: use `search_replace` for targeted fixes

**Re-run hooks:**
```
run_terminal_cmd: {same hook command}
```

**If still failing:**
Show user the errors and ask:
- "Continue anyway?" (for minor issues)
- "Let me fix manually first" (user takes over)
- "Skip commit for now"

6) Propose commit message:
   - 1 primary + up to 2 alternatives
   - follow `<type>(<scope>): <subject>`
   - include BREAKING CHANGE footer if needed

7) Ask for explicit approval.

8) If approved:
   - `run_terminal_cmd`: `git commit -m "..."` (and body/footer if needed)
   - `run_terminal_cmd`: `git push`

## Output
- Proposed message(s)
- Hooks run + result
- Commands that will run if you approve
