---
name: commit
description: Stage, test, and commit with conventional message
---

# Commit Helper (Conventional Commits + Hooks)

## What This Workflow Does

Fully automated commit flow — runs start to finish without interruption.
**The only question asked is at the very end: approve the commit message and push.**

### ✅ DOES:
- Auto-stages all unstaged changes (`git add -A`)
- Shows changed files list (`--stat` only, no full diff)
- Runs pre-commit hooks automatically
- Auto-fixes lint/format errors without asking
- Generates a single best-fit Angular Conventional Commit message
- Asks once for approval, then commits and pushes
- Updates the GitLab MR description with a progress snapshot

### ❌ DOES NOT:
- Does NOT show full diffs
- Does NOT ask for staging confirmation
- Does NOT ask multiple approval questions
- Does NOT write code, create branches, or merge

## Steps

### 1 — Gather facts (silently, in parallel)

```
git status --short
git diff --stat          # unstaged
git diff --staged --stat # already staged
git log --oneline -5     # recent context for message style
read_file: memory-bank/current-mr.md
```

### 2 — Auto-stage everything

If there are any unstaged changes (tracked or untracked relevant files):
```
git add -A
```
Do **not** ask for confirmation. Do **not** pause.

Then collect the staged file list:
```
git diff --staged --stat
git diff --staged --name-only
```

If there is nothing to stage and nothing already staged → tell the user and stop.

### 3 — Run pre-commit hooks (auto)

Read `precommit_runner` from `memory-bank/current-mr.md`.

| Value | Command |
|---|---|
| `lint-staged` | `npx lint-staged` |
| `pre-commit` | `pre-commit run --files {staged files}` |
| `both` | run lint-staged then pre-commit |
| `null` / missing | check for `.pre-commit-config.yaml` or `package.json → lint-staged`; run if found, skip if not |

If hooks are not installed: skip silently.

### 4 — Auto-fix hook failures (no questions asked)

If hooks fail, immediately attempt auto-fixes based on the error output:

| Error type | Fix command |
|---|---|
| ESLint errors | `npx eslint --fix {files}` |
| Prettier formatting | `npx prettier --write {files}` |
| Black (Python) | `black {files}` |
| isort | `isort {files}` |

After auto-fixing, re-stage fixed files (`git add {fixed files}`) and re-run hooks once.

**If hooks still fail after auto-fix** — and only then — show the errors and ask:
> "Hooks still failing. Continue anyway, or stop so you can fix manually? [continue/stop]"

### 5 — Generate commit message

Analyse the staged diff (`git diff --staged`) and produce exactly **one** commit message:
- Format: `<type>(<scope>): <subject>`
- Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- Subject: imperative mood, ≤50 chars, no trailing period
- Add body (what + why) if the change is non-trivial
- Add `BREAKING CHANGE:` footer if applicable

Do not present alternatives. Pick the best one.

### 6 — Single approval gate

Show a compact summary — **this is the only prompt in the workflow**:

```
─────────────────────────────────────────
  Files staged:
  {output of git diff --staged --stat}

  Commit message:
  {proposed message}

  Push to: {remote}/{branch}
─────────────────────────────────────────
  Approve and push? [Y/n] (or type a new message):
```

Behaviour:
- **Y / Enter** → commit and push immediately
- **n** → stop, do nothing
- **Custom text typed** → use that text as the commit message, then commit and push

### 7 — Commit and push

```
git commit -m "{message}"
git push -u origin {branch}
```

If push fails due to no upstream: `git push --set-upstream origin {branch}`.

### 8 — Update MR description (after push, no user input needed)

Find the active MR for the current branch:
```
read_file: memory-bank/current-mr.md
git branch --show-current
```
Match current branch → `merge_requests` list. If no match, skip silently.

Read story context if available:
```
read_file: memory-bank/story.md (if exists)
```

Fetch commits:
```
git log --oneline origin/{base_branch}...HEAD
```

Build and inject progress block into the MR description:
```markdown
<!-- PROGRESS:START — updated automatically by commit workflow, do not edit this block manually -->
## 🔄 Progress (auto-updated)

**Last commit:** {commit message} (`{short sha}`)
**Updated:** {datetime}
**Branch:** {feature_branch} → {base_branch}

### Recent commits
{git log output, newest first, max 10}

### Task progress (from story.md)
{N / M tasks completed — brief list, only if story.md exists}
<!-- PROGRESS:END -->
```

- Replace existing `PROGRESS:START…PROGRESS:END` block if present, otherwise append
- Use `gitlab_update_merge_request` to write back
- If MCP unavailable: note it briefly, do not block or revert the commit

## Output

- Changed files list shown once
- One commit message shown once
- One approval prompt
- Committed, pushed, MR description updated
