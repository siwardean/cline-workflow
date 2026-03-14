# Workflow Reference

Five workflows cover the entire feature lifecycle. Run them by telling your AI assistant:
> _"Run the [name].md workflow"_

---

## Overview

| Workflow | When | Touches GitLab? | Touches code? |
|---|---|---|---|
| **start.md** | Once, before development begins | Yes — creates MR | No |
| **morning.md** | Every morning | Yes — updates MR descriptions | No |
| **commit.md** | After each set of code changes | Yes — updates MR progress | No (only commits) |
| **review.md** | When asked to review an MR | Yes — posts discussion threads | No |
| **close.md** | Once, after MR is merged | Read-only | No |

---

## start.md — Feature Planning

**Trigger:** You have a new story ready to work on.

```
You → AI: story title + description + acceptance criteria
AI  → You: execution plan (5–12 tasks)
You → AI: approve or request changes
AI  → Git + GitLab: branch created, MR opened
```

### What the AI does, step by step

```mermaid
flowchart TD
    A[Read memory-bank/current-mr.md] --> B[Ask for story title + description + ACs]
    B --> C[Search codebase for relevant files]
    C --> D[Build 5–12 task execution plan]
    D --> E{Present plan for review}
    E -->|Changes requested| D
    E -->|Approved| F[Derive branch name from keywords]
    F --> G[git checkout -b feature/slug && git push]
    G --> H[Create Draft MR via GitLab MCP]
    H --> I[Write memory-bank/story.md]
    I --> J[Update memory-bank/current-mr.md]
    J --> K[Confirm: branch + MR IID to developer]
```

### Branch naming (enforced by rules.md)

Format: `feature/<keyword>_<keyword>_<keyword>`
Keywords come from the story title — meaningful nouns/verbs only, no generics.

| Story | Branch |
|---|---|
| "Reset password via email" | `feature/password_reset_email` |
| "Paginate product listing" | `feature/product_listing_pagination` |
| "Stripe subscription billing" | `feature/stripe_subscription_billing` |

### Plan format

Each task in the plan has:
- Files to create or modify
- Tests to write
- Acceptance criteria it covers
- SonarQube risks to watch
- Definition of done

### Key rule: nothing is created until you approve the plan.

---

## morning.md — Daily Ritual

**Trigger:** Start of your workday — run this before anything else.

This workflow does **two things in sequence**: closes out yesterday, then sets up today.

```mermaid
sequenceDiagram
    participant AI
    participant Git
    participant GitLab
    participant SonarQube

    Note over AI,SonarQube: Phase 1 — wrap up yesterday

    AI->>Git: git log last 24h, git diff vs base
    AI->>SonarQube: quality gate, coverage, new issues
    AI->>GitLab: update all MR descriptions (from MR template + story.md)
    AI->>GitLab: fetch open reviewer threads
    AI->>AI: draft professional replies per thread
    AI->>AI: write memory-bank/handover.md

    Note over AI,SonarQube: Phase 2 — start today

    AI->>GitLab: fetch fresh MR status + pipeline for each MR
    AI->>SonarQube: fetch fresh quality gate + issues
    AI->>AI: prioritise by severity
    AI-->>Developer: full morning report + thread drafts
```

### Morning report includes

- SonarQube quality gate (pass/fail, coverage %)
- Per-MR: pipeline status, unresolved thread count, priority rating
- Today's task list (ordered by priority)
- Thread reply drafts ready to copy/paste into GitLab

### What it does NOT do

- Does not post replies to GitLab (you copy/paste the drafts)
- Does not resolve threads
- Does not commit anything

---

## commit.md — Commit Helper

**Trigger:** You have code changes ready to commit.

```mermaid
flowchart TD
    A[git status + git diff] --> B{Any staged changes?}
    B -->|No| C[Propose files to stage]
    C --> D{You confirm staging}
    B -->|Yes| E[Show staged diff]
    D --> E
    E --> F[Run pre-commit hooks]
    F --> G{Hooks pass?}
    G -->|Lint/format errors| H[Auto-fix with ESLint/Prettier/Black]
    H --> F
    G -->|Unfixable| I[Show errors — you decide]
    G -->|Pass| J[Propose 1–3 commit messages]
    J --> K{You approve message}
    K -->|No| J
    K -->|Yes| L[git commit && git push]
    L --> M[Update MR progress block via GitLab MCP]
```

### Hook support

Configured in `memory-bank/current-mr.md` → `precommit_runner`:

| Value | What runs |
|---|---|
| `lint-staged` | `npx lint-staged` |
| `pre-commit` | `pre-commit run --files ...` |
| `both` | Both in sequence |
| `null` | Auto-detect from project config |

### Commit message format (Angular Conventional Commits)

```
<type>(<scope>): <subject>

<body — what and why, not how>

<footer — BREAKING CHANGE: ... if applicable>
```

Types: `feat` `fix` `docs` `style` `refactor` `perf` `test` `build` `ci` `chore` `revert`

### MR progress block

After every push, the AI injects a `<!-- PROGRESS:START -->` block into the MR description with:
- Last commit message + SHA
- Recent commit list (newest first, max 10)
- Task progress from `story.md` (N / M tasks done)

If GitLab MCP is unavailable, the commit still goes through — the MR update is best-effort.

---

## review.md — MR Code Review

**Trigger:** You're asked to review someone else's MR (or your own before asking for approval).

```mermaid
flowchart TD
    A[Detect branch / prompt for MR IID] --> B[Fetch MR metadata + discussions via GitLab MCP]
    B --> C[git diff: fetch full diff]
    C --> D[Assess existing open threads]
    D --> E{Code changed after thread?}
    E -->|Yes| F[Mark: Addressed by code]
    E -->|No| G{Author replied?}
    G -->|Yes| H[Mark: Addressed by reply]
    G -->|No| I[Mark: Needs attention]
    F & H & I --> J[Perform code review on diff]
    J --> K[Present findings table]
    K --> L{Which to post?}
    L -->|Selected| M[Post as GitLab discussion threads]
    L -->|None| N[Skip posting]
    M & N --> O[Print summary]
```

### Review categories

| Category | Examples |
|---|---|
| 🔴 Bug | Null dereference, off-by-one, swallowed exception |
| 🔴 Security | SQL injection, hardcoded secret, missing auth check |
| 🟠 Performance | N+1 query, unbounded loop, missing index |
| 🟡 Style | Generic name, duplicated logic, dead code |
| 🔵 Tests | Missing coverage for new path, implementation-coupled assertions |
| 🔵 Docs | Undocumented public API change |

### Thread assessment

For each existing open thread, classifies as:
- `✅ Addressed by code` — the relevant file/area was changed after the thread was opened
- `💬 Addressed by reply` — the MR author replied to the reviewer
- `⚠️ Needs attention` — no code change or reply since the thread was opened

### Single approval gate

After showing all findings, asks once which to post. Everything else runs automatically.

### What it does NOT do

- Does not approve or merge the MR
- Does not resolve threads
- Does not write or fix code
- Does not post anything without your selection

---

## close.md — Post-Merge Retrospective

**Trigger:** Your MR has been merged in GitLab. Run this to capture learnings.

```mermaid
flowchart TD
    A[Read memory-bank/story.md + current-mr.md] --> B[Fetch merged MR from GitLab MCP]
    B --> C{MR state = merged?}
    C -->|No| D[Warn user and ask to continue]
    C -->|Yes| E[Fetch MR discussions + final pipeline]
    E --> F[git fetch — find merge commit]
    F --> G[Compare plan vs actual delivery]
    G --> H[Evaluate each AC: Met / Partial / Not met]
    H --> I[Calculate time variance]
    I --> J[Summarise reviewer feedback themes]
    J --> K[Write memory-bank/retro.md]
    K --> L[Show retrospective to developer]
```

### Retrospective covers

| Section | What's in it |
|---|---|
| AC compliance | Each criterion: met/partial/not met + evidence |
| Plan vs reality | Tasks completed as planned vs skipped vs unplanned |
| Time variance | Estimated days vs actual calendar days + reasons |
| Quality | Final coverage %, SonarQube status, reviewer themes |
| Lessons learned | What went well, what to improve, root causes |
| Recommendations | Actionable items for the next feature |

### What it does NOT do

- Does not merge the MR — you do that in GitLab UI
- Does not modify any source code
- Does not update GitLab (read-only)

---

## Shared Rules

These apply across all workflows. Full details in `rules.md`.

- **MCP errors**: always handled gracefully — workflow continues, user is informed
- **Approval gates**: commits and MR creation require explicit user confirmation
- **memory-bank files**: `handover.md`, `story.md`, `retro.md` are gitignored — local AI state only, never committed to the project repo
- **MR template**: `eod` and `morning` updates follow `.gitlab/merge_request_templates/default.md`
- **SonarQube**: always fetch quality gate, coverage, bugs, vulnerabilities, code smells — results drive priorities
