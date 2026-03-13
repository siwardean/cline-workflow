---
name: start
description: Plan a user story, then auto-create the git branch and GitLab MR
---

# Feature Start (User Story → Plan → Branch → MR)

## What This Workflow Does

**Takes your user story, builds an execution plan, waits for your approval, then creates the branch and MR automatically.**

### ✅ DOES:
- Asks you for the story title, description, and acceptance criteria (that's all you need to provide)
- Searches the codebase for relevant code
- Creates a 5-12 task execution plan mapped to acceptance criteria
- **Presents the plan for your review** — nothing is created until you approve
- Creates the git feature branch locally and pushes it
- Creates the GitLab MR via MCP with a concise plan in the description
- Writes the full plan to `memory-bank/story.md`
- Updates `memory-bank/current-mr.md` with the new MR details

### ❌ DOES NOT:
- Does NOT create branch or MR without your explicit approval of the plan
- Does NOT write production code
- Does NOT modify any existing source files

## Prerequisites
- `memory-bank/current-mr.md` exists with at least `project_id` and `base_branch`
- GitLab MCP server configured and reachable
- You are on the base branch (e.g., `main`) or a clean state

## Input (you provide in chat)

Just tell your AI assistant the following — no specific format required:

```
Story title: <short title>
Description: <what the feature does and why>
Acceptance criteria:
  1. <AC 1>
  2. <AC 2>
  3. ...
```

That's it. Your AI assistant handles everything else.

## Output
- `memory-bank/story.md` — Full execution plan (tasks, tests, risks)
- `memory-bank/current-mr.md` — Updated with new MR IID and feature branch
- Git feature branch pushed to origin
- GitLab MR created with a concise implementation plan in the description

---

## Steps (tool-first)

### 1) Read workspace state
```
read_file: memory-bank/current-mr.md
run_terminal_cmd: git status
run_terminal_cmd: git branch --show-current
```

Extract: `project_id`, `base_branch`. If missing, stop and ask the user to set them in `memory-bank/current-mr.md`.

### 2) Collect the user story

If the user has not already provided it, ask for:
- **Title** — one short sentence (becomes the branch name slug and MR title)
- **Description** — what the feature does and why it is needed
- **Acceptance Criteria** — numbered list; at least one required

Derive a branch slug from the title:
```
slug = title.lower().replace(' ', '-').strip('-')
feature_branch = f"feature/{slug}"
```

### 3) Ground in the codebase

```
run_terminal_cmd: git fetch origin
run_terminal_cmd: git log --oneline origin/{base_branch} -10
```

Extract 2–4 key terms from the title/description (e.g., "authentication", "export", "payment").

For each term, search for relevant files:
```
run_terminal_cmd: git grep -l "{term}" -- '*.ts' '*.tsx' '*.js' '*.jsx' '*.py' '*.java' '*.go'
```

Discover top-level structure:
```
list_dir: src   (or the appropriate source directory)
```

Read at most 2–3 of the most relevant files to understand architecture — do not read entire files unless necessary.

**If no files match:** that's fine, this may be a brand-new feature area.

### 4) Build the execution plan

**Analyze requirements:**
- Break down each Acceptance Criterion
- Identify the technical approach
- Estimate complexity (simple / medium / complex)
- Note dependencies and edge cases

**Create 5–12 tasks, each with:**

```
Task {N}: {Action verb} {What}
- ACs covered: [{AC numbers}]
- Files/modules:
  - {file path} (create / modify)
- Tests:
  - {test file} (create / modify)
  - Test cases: [{brief list}]
- SonarQube risks: {complexity, duplication, security concerns}
- Definition of Done: {specific, testable criteria}
```

**AC coverage map:**
```
AC1 → Tasks [N, M]
AC2 → Tasks [P]
...
```

**Test strategy summary:**
- Unit tests: {what to cover}
- Integration tests: {if needed}
- Coverage target: maintain or improve current %

**Validate plan quality (internal check before presenting):**
- ✅ Every AC is covered by at least one task
- ✅ Every task has at least one test
- ✅ No vague tasks — each is actionable
- ✅ Dependencies between tasks are explicit

### 5) Present plan for developer review

Display the full plan clearly in chat, then ask:

```
📋 Execution Plan ready for: "{story title}"

[... display full plan ...]

Do you approve this plan?
- ✅ Yes — I'll create the branch and MR now
- ✏️  No — tell me what to change and I'll revise

Your call before anything is created.
```

**STOP HERE and wait for the developer's response.**

- If the developer requests changes, revise the plan and present it again (repeat until approved).
- Only proceed to Step 6 after explicit approval.

### 6) Summarise the plan (concise MR description)

Once approved, produce a **concise plan summary** (max ~20 lines) to use as the MR description:

```markdown
## Implementation Plan

**Story:** {title}

**Description:** {one-paragraph summary}

### Acceptance Criteria
1. {AC 1}
2. {AC 2}
...

### Key Tasks
1. {Task 1 — one line}
2. {Task 2 — one line}
...

### Test Strategy
- {Unit / integration / e2e summary}

### Risks
- {Main risks or "None identified"}
```

### 7) Create the feature branch

```
run_terminal_cmd: git checkout {base_branch}
run_terminal_cmd: git pull origin {base_branch}
run_terminal_cmd: git checkout -b {feature_branch}
run_terminal_cmd: git commit --allow-empty -m "feat: initialize {slug}"
run_terminal_cmd: git push -u origin {feature_branch}
```

**Error handling:** If the branch already exists, inform the user and ask whether to reuse it or pick a different name.

### 8) Create the GitLab MR via MCP

**List MCP tools available** to discover exact tool names, then create the MR:

```
gitlab_create_merge_request (or equivalent tool):
  project_id: {project_id}
  source_branch: {feature_branch}
  target_branch: {base_branch}
  title: "feat: {story title}"
  description: {concise plan summary from Step 6}
  draft: true
```

Capture the returned `mr_iid` from the MCP response.

**Error handling:** If MCP creation fails, show the user the concise plan and the git commands — they can create the MR manually in GitLab.

### 9) Update memory-bank files

**Update `memory-bank/current-mr.md`** — append the new MR to the `merge_requests` list:

```yaml
merge_requests:
  # ... existing entries ...
  - mr_iid: {mr_iid}
    feature_branch: {feature_branch}
    description: "{story title}"
```

**Write `memory-bank/story.md`** with the full execution plan (all details from Step 4).

### 10) Confirm to the developer

```
✅ Feature setup complete!

Branch:  {feature_branch}  (pushed to origin)
MR:      !{mr_iid} — "{story title}"  (Draft, target: {base_branch})
Plan:    memory-bank/story.md

Next steps:
1. Run the morning.md workflow each morning to check MR status
2. Ask your AI assistant to implement Task 1: "{first task title}"
3. Run commit.md after each set of changes
4. Run eod.md at end of day to update the MR description
```

## Success Criteria
- Developer only typed their story information — no manual git or GitLab steps
- Plan was reviewed and approved before any branch or MR was created
- MR description contains the concise approved plan
- `memory-bank/story.md` and `memory-bank/current-mr.md` are up to date
