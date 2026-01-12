# /start.md — Start Feature (manual Rally story input)

## Objective
Turn a **Rally user story** (provided manually) into an execution plan aligned with:
- Description / Notes
- Acceptance Criteria
- Estimate (man-days)
- Clean Code + Tests/Coverage + SonarQube quality gates

## Inputs (you provide in chat)
Paste the Rally story in this format:

- Title:
- Description:
- Notes: (optional)
- Acceptance Criteria:
  1) ...
  2) ...
- Estimate (man-days): X

## Steps (tool-first)

### 1) Read workspace state
```
read_file: memory-bank/current-mr.md
run_terminal_cmd: git status
run_terminal_cmd: git branch --show-current
```

Validate configuration is present. If missing fields, stop and ask user to configure.

### 2) Minimal repo grounding
```
run_terminal_cmd: git fetch origin
run_terminal_cmd: git log --oneline origin/{base_branch} -20
```

**Search for relevant code:**
Extract 2-4 key terms from story title/description (e.g., "password", "authentication", "export")

For each term:
```
run_terminal_cmd: git grep -l "{term}" -- '*.ts' '*.tsx' '*.js' '*.jsx' '*.py' '*.java'
```

**Error handling:** If grep returns no results, that's OK - might be a new feature.

**Discover structure:**
```
list_dir: src (or appropriate source directory)
```

**Read key files** (only 2-3 most relevant):
```
read_file: [discovered entrypoint or related module]
```

Limit file reading to understand architecture, not implementation details.

### 3) Produce execution plan

**Analyze requirements:**
- Break down each Acceptance Criterion
- Identify technical approach
- Estimate complexity
- Consider edge cases

**Create 5–12 tasks, each with:**

```
Task {N}: {Action verb} {What}
- ACs covered: [{AC numbers}]
- Files/modules: 
  - {file path} (create/modify)
  - {file path}
- Tests:
  - {test file} (create/modify)
  - Test cases: [{brief list}]
- Docs:
  - README.md: {what to update} (if user-facing)
- SonarQube risks:
  - {potential issues: complexity, duplication, security}
- Definition of Done:
  - {specific, testable criteria}
```

**Coverage map:**
```
AC1 → Tasks [{numbers}]
AC2 → Tasks [{numbers}]
...
```

**Test strategy:**
- Unit tests: {what to cover}
- Integration tests: {what to cover}
- E2E tests: {if needed}
- Coverage target: maintain or improve current %

**SonarQube considerations:**
- Complexity hotspots: {where to watch}
- Duplication risks: {where to avoid}
- Security concerns: {if any}

### 4) Validate plan quality

**Check:**
- ✅ All ACs covered by at least one task
- ✅ Every task has tests
- ✅ Plan is actionable (no vague tasks)
- ✅ Complexity estimated (simple/medium/complex per task)
- ✅ Dependencies identified

### 5) Write baseline
```
write: memory-bank/story.md
```

Use the template structure from current story.md but fill with real plan.

## Output format
- Plan (numbered)
- AC coverage map (AC → tasks)
- Test plan + coverage notes
- SonarQube/quality-gate risk notes
- Open questions/assumptions
