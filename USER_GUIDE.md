# 🚀 User Guide: Your First Week with Cline Workflows

**Welcome!** This guide will help you get started with AI-assisted development using Cline and this workflow kit. No prior experience with AI agents needed!

---

## 📖 Table of Contents

1. [What is This?](#what-is-this)
2. [How to Talk to Cline](#how-to-talk-to-cline)
3. [Your First Feature: Step-by-Step](#your-first-feature-step-by-step)
4. [Daily Workflow Examples](#daily-workflow-examples)
5. [Common Scenarios](#common-scenarios)
6. [Tips & Tricks](#tips--tricks)
7. [Troubleshooting](#troubleshooting)

---

## What is This?

### Traditional Development
You write code, run tests, check SonarQube, update MRs, respond to reviewers... manually.

### With Cline + This Kit
You work **with an AI pair programmer** that:
- Reads your GitLab MR threads for you
- Checks SonarQube quality gates automatically
- Drafts responses to reviewer comments
- Helps you write commit messages
- Updates your MR description
- Tracks your progress

**Think of Cline as a very helpful junior developer who never gets tired and loves documentation.** 🤖

---

## 📂 Where Do These Files Go?

**IMPORTANT:** These files go in your **project root** (workspace root):

```
your-project/                    ← Open THIS folder in VS Code
├── .clinerules/                 ← Cline reads automatically
│   ├── rules.md                 ← Workspace rules
│   └── workflows/               ← Your workflows
│       ├── morning.md
│       ├── eod.md
│       └── ...
├── memory-bank/                 ← Project state
│   ├── current-mr.md
│   └── ...
├── README.md
└── ...
```

**How it works:**
1. You open the project folder in VS Code (File → Open Folder)
2. Cline automatically discovers `.clinerules/rules.md` in the workspace root
3. Workflows become available immediately
4. No configuration needed!

**Common mistake:**
- ❌ Opening a parent directory that contains your project
- ❌ Opening just individual files
- ✅ Opening the actual project folder where `.clinerules/` exists

---

## How to Talk to Cline

### Opening Cline
1. Open VS Code IDE
2. Look for the **Cline** icon in the left sidebar (or press `Ctrl/Cmd + Shift + P` and type "Cline")
3. The Cline chat window opens on the right

### Running Workflows

Workflows are like **pre-written instructions** for Cline. Instead of explaining what you want every time, just reference the workflow file.

**Three ways to run a workflow:**

#### Method 1: Type in Chat (Recommended)
```
Run the morning.md workflow
```

#### Method 2: Use @ to Reference
```
@morning.md please run this workflow
```

#### Method 3: Natural Language
```
I want to start my day by checking MR threads and SonarQube status
```
_(Cline will figure out you want the morning workflow)_

---

## Your First Feature: Step-by-Step

Let's walk through building a complete feature, from story to merge.

### 📅 **Day 1: Starting the Feature**

#### Step 1: Get Your Story Ready
Copy your user story from Rally/Jira. It should look like:

```
Title: Add password strength indicator
Description: Users need visual feedback when creating passwords
Acceptance Criteria:
  1) Show strength meter (weak/medium/strong)
  2) Display requirements (8+ chars, number, special char)
  3) Meter updates in real-time as user types
Estimate: 2 man-days
```

#### Step 2: Tell Cline to Start
**You say:**
```
Run the start.md workflow. Here's my story:

Title: Add password strength indicator
Description: Users need visual feedback when creating passwords
Acceptance Criteria:
  1) Show strength meter (weak/medium/strong)
  2) Display requirements (8+ chars, number, special char)
  3) Meter updates in real-time as user types
Estimate: 2 man-days
```

#### Step 3: Watch Cline Work
Cline will:
1. ✅ Read your current MR configuration
2. ✅ Check your git status
3. ✅ Search the codebase for relevant files (password, auth, forms)
4. ✅ Create a task plan in `memory-bank/story.md`

#### Step 4: Review the Plan
Cline shows you something like:

```
📋 Execution Plan

Task 1: Create password strength calculation logic
- Files: src/utils/password-validator.ts
- Tests: password-validator.spec.ts
- AC: [1, 2]

Task 2: Build strength meter component
- Files: src/components/PasswordStrengthMeter.tsx
- Tests: PasswordStrengthMeter.test.tsx
- AC: [1, 3]

Task 3: Integrate into registration form
- Files: src/pages/RegisterPage.tsx
- Tests: RegisterPage.test.tsx
- AC: [1, 2, 3]

Task 4: Update documentation
- Files: README.md
```

**You can now:**
- Ask questions: "Why did you choose these files?"
- Request changes: "Can we split Task 2 into two smaller tasks?"
- Start coding: "Let's start with Task 1"

---

### 🌅 **Day 2: Morning Check-in**

#### You arrive at work. What's the status?

**You say:**
```
Run the morning.md workflow
```

#### Cline Shows You:
```
🔍 MR Status for !67

GitLab Threads:
📌 Thread #1 (unresolved) - src/utils/password-validator.ts:15
   Reviewer: @sarah
   "Should we support passphrases (longer than 20 chars)?"
   
📌 Thread #2 (resolved) - README.md
   Reviewer: @mike
   "Please add example usage" ✅ FIXED

Pipeline: ✅ PASSING (run #1234)

SonarQube Quality Gate: ✅ PASS
- Coverage: 87.3% (+2.1%)
- 0 bugs, 0 vulnerabilities
- 1 code smell (minor): "Consider extracting complexity"

📅 Today's Plan:
1. Address Sarah's question about passphrases
2. Refactor complexity issue in password validator
3. Add integration tests for registration flow
```

**Now you know exactly what to work on!**

---

### 💻 **Working on Code**

#### Example: Implementing a Task

**You say:**
```
Let's implement Task 1: password strength calculation.
I want to check for:
- Minimum 8 characters
- At least 1 number
- At least 1 special character
- Return weak/medium/strong
```

**Cline will:**
1. Create `src/utils/password-validator.ts`
2. Write the logic with proper TypeScript types
3. Create corresponding test file
4. Run the tests
5. Show you the results

**You review and say:**
```
Looks good! But let's also check for uppercase letters.
```

Cline updates the code.

---

### ✅ **Making a Commit**

#### When You're Ready to Commit

**You say:**
```
Run the commit.md workflow
```

**Cline will:**
1. Show you `git status`
2. Show you `git diff` of your changes
3. Ask if you want to stage anything specific
4. Run pre-commit hooks (lint, tests)
5. Propose a commit message:

```
🎯 Proposed Commit Messages:

Primary:
feat(auth): add password strength validator

Validates password strength based on length, character types,
and complexity. Returns weak/medium/strong rating.

BREAKING CHANGE: None

Alternatives:
1. feat(auth): implement password strength meter logic
2. feat(utils): add password validation utility
```

**You say:**
```
Use the primary message and commit
```

Cline commits and pushes! 🎉

---

### 🌆 **End of Day: Update MR**

#### Before Logging Off

**You say:**
```
Run the eod.md workflow
```

**Cline will:**
1. ✅ Fetch latest SonarQube results
2. ✅ Update your MR description (filling the template)
3. ✅ Draft replies to resolved threads:

```
📝 Draft Reply to Thread #2 (Sarah's question):

"Good point! I've updated the validator to support passphrases up to 128 characters.

Changes:
- Modified `validatePasswordStrength()` to accept 8-128 chars
- Added test cases for long passphrases
- Updated README with passphrase examples

Tests: Run `npm test password-validator.spec.ts`
Proof: All tests passing (see pipeline #1235)

Can you confirm this addresses your concern?"
```

4. ✅ Update `memory-bank/handover.md` with today's progress

**You review, copy the draft reply to GitLab, and go home!** 🏡

---

## Daily Workflow Examples

### Monday Morning
```
Run the morning.md workflow
```
**Result:** Status update, threads, SonarQube, plan for the day

### After Code Changes
```
Run the commit.md workflow
```
**Result:** Staged changes, hooks run, commit message proposed

### End of Day
```
Run the eod.md workflow
```
**Result:** MR updated, threads addressed, handover written

### After MR Merges
```
Run the close.md workflow
```
**Result:** Retrospective written, comparing plan vs reality

---

## Common Scenarios

### Scenario 1: "I Have Reviewer Comments"

**You say:**
```
What are my unresolved MR threads?
```

**Cline shows you the threads, you can then say:**
```
Let's address the first thread about error handling
```

Cline will help you implement the fix.

---

### Scenario 2: "SonarQube is Failing"

**You say:**
```
What's blocking the SonarQube quality gate?
```

**Cline responds:**
```
Quality Gate: FAIL

Issues:
1. Bug (High): Potential null pointer in UserService.ts:45
2. Vulnerability (Medium): SQL injection risk in query.ts:89
3. Code Smell: Cognitive complexity in handleLogin()

Let's fix these one by one?
```

**You say:**
```
Start with the bug in UserService
```

---

### Scenario 3: "I Forgot What I Was Working On"

**You say:**
```
What's my current status? Read the handover file.
```

**Cline shows you:**
```
Last Handover (2026-01-11)

✅ Implemented: Password strength validator, meter component
🔄 In Progress: Integration tests
📋 Not Started: Documentation update

Next Steps:
1. Finish integration tests for registration flow
2. Address Sarah's thread about passphrases
3. Update README with usage examples
```

---

### Scenario 4: "I Need to Search the Codebase"

**You say:**
```
Where do we handle user authentication in this codebase?
```

Cline will search and show you relevant files.

---

### Scenario 5: "I Want to Refactor Something"

**You say:**
```
The validatePassword function is getting complex. Can you help me refactor it into smaller functions?
```

Cline will:
1. Read the current code
2. Propose a refactoring plan
3. Show you the before/after
4. Update tests
5. Run tests to ensure nothing broke

---

## Tips & Tricks

### 🎯 **Tip 1: Be Specific**
❌ "Fix the bug"
✅ "Fix the null pointer exception in UserService.ts line 45"

### 🎯 **Tip 2: One Task at a Time**
❌ "Update the MR, fix SonarQube, and refactor three files"
✅ "Let's start by fixing the SonarQube issues, then we'll update the MR"

### 🎯 **Tip 3: Review Before Approving**
When Cline proposes changes:
1. Read the diff
2. Ask questions if unclear
3. Request changes if needed
4. Only then approve

### 🎯 **Tip 4: Use Memory Bank**
The `memory-bank/` folder is your **shared memory** with Cline:
- `story.md` = What you're building
- `handover.md` = Current status
- `current-mr.md` = Configuration

Update these manually if needed!

### 🎯 **Tip 5: Teach Cline Your Preferences**
```
When writing commit messages, I prefer the scope to be the feature name, not the file type.
So use "feat(password-strength)" instead of "feat(auth)"
```

Cline will remember for this session!

### 🎯 **Tip 6: Ask for Explanations**
```
Why did you choose this approach?
What does this code do?
Can you explain the SonarQube issue in simple terms?
```

Cline is great at explaining things!

---

## Troubleshooting

### Problem: "Cline doesn't see my MR threads"

**Check:**
1. Is GitLab MCP configured? Run `python validate_mcp_setup.py`
2. Is `project_id` and `mr_iid` correct in `memory-bank/current-mr.md`?
3. Does your GitLab token have `api` scope?

**Fix:**
```
Update memory-bank/current-mr.md with the correct values, then run:
Run the morning.md workflow again
```

---

### Problem: "Cline says it can't read files"

**Solution:**
Cline might not have the right file path. Be specific:

❌ "Read the auth file"
✅ "Read the file src/auth/AuthService.ts"

---

### Problem: "The commit workflow isn't running hooks"

**Check:**
1. Open `memory-bank/current-mr.md`
2. Set `precommit_runner` to your hook type:
   - `"lint-staged"` if you use lint-staged
   - `"pre-commit"` if you use pre-commit framework
   - `"both"` if you use both
   - `null` if you have no hooks

---

### Problem: "I don't understand what Cline is doing"

**Just ask!**
```
Can you explain what you're doing step by step?
```

or

```
Slow down and show me each change before applying it
```

---

### Problem: "Cline made a mistake"

**No problem!** You can:

1. **Undo with git:**
   ```
   Undo that last change
   ```

2. **Give feedback:**
   ```
   That's not quite right. I wanted you to add validation, not remove it.
   ```

3. **Start over:**
   ```
   Let's start this task from scratch
   ```

---

## 🎓 Learning More

### Understanding the Workflows

Each workflow is just a markdown file in `.clinerules/workflows/`. You can:

1. **Read them:** Open the files to see what Cline will do
2. **Customize them:** Edit to match your team's process
3. **Create new ones:** Add your own workflows!

### Example: Reading a Workflow

Open `.clinerules/workflows/morning.md`:

```markdown
# /morning.md — Sonar-driven planning

## Objective
Plan remediation work using SonarQube results.

## Steps
1) Read MR context.
2) Fetch MR threads and pipeline status.
3) Fetch SonarQube: Bugs, Vulnerabilities, Code Smells...
```

**This tells Cline exactly what to do when you say "Run morning.md"**

---

## 🎉 You're Ready!

### Your First Day Checklist

- [ ] Run `python validate_mcp_setup.py`
- [ ] Update `memory-bank/current-mr.md` with your project details
- [ ] Try: "Run the morning.md workflow"
- [ ] Ask Cline: "What files are in this project?"
- [ ] Practice: Make a small change and use the commit workflow

### Remember

- **Cline is your assistant, not your boss.** You're in control!
- **Start small.** Try one workflow at a time.
- **Ask questions.** Cline loves to explain things.
- **Review everything.** Trust, but verify.

---

## Need Help?

**Talk to Cline like a colleague:**
```
I'm new to this workflow system. Can you give me a beginner-friendly overview of what these workflows do?
```

**Or ask specific questions:**
```
How do I update my MR description?
What's the difference between morning.md and eod.md?
Can you show me an example of a good commit message?
```

---

**Happy coding! 🚀**

You've got a powerful AI pair programmer on your team now. Take advantage of it, but remember: you're the senior developer. Cline is here to handle the tedious stuff so you can focus on the creative problem-solving! 💡

