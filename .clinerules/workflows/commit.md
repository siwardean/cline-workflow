# /commit.md — Commit Agent (Conventional Commits + pre-commit)

## Objective
Prepare a clean commit by:
- ensuring the right changes are staged
- running pre-commit hooks / lint-staged
- proposing the best Angular Conventional Commit message
- committing + pushing ONLY after user approval

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
