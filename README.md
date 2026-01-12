# Cline GitLab Feature Workflow Kit

A minimal, **workflow-driven** setup for using Cline with:
- GitLab Merge Requests (via local GitLab MCP)
- SonarQube (via local Sonar MCP)
- Daily **morning** planning and **EOD** MR updates
- Reviewer thread tracking + draft replies
- Angular Conventional Commits for semantic-release
- Clean Code + tests/coverage + SonarQube quality gates
- Project contribution governance

---

## 👋 New to AI Coding Assistants?

**Welcome!** If you've never used an AI agent like Cline before, don't worry - it's easier than you think!

**Think of Cline as your helpful pair programmer** who:
- ✅ Never gets tired of checking SonarQube
- ✅ Loves writing commit messages
- ✅ Remembers to update your MR description
- ✅ Keeps track of reviewer comments for you

**You're still in charge!** You write the features, make the decisions. Cline just handles the tedious stuff.

### 📚 Learning Resources

**Start here:**
- **[User Guide](user-guide.md)** - Step-by-step walkthrough of your first feature (15 min read)
- **[Quick Reference](docs/quick-reference.md)** - Cheat sheet for common tasks (keep it handy!)
- **[Workflow Examples](docs/workflow-examples.md)** - See real examples of each workflow in action

**Quick Examples:**

| You say to Cline | What happens |
|------------------|--------------|
| `Run the morning.md workflow` | Shows you MR status, reviewer comments, SonarQube results |
| `Run the commit.md workflow` | Runs tests, proposes commit message, commits if you approve |
| `Run the eod.md workflow` | Updates your MR, drafts replies to reviewers |

**Your first command:** Just say "Run the morning.md workflow" and Cline will check your MR status!

---

## Folder structure

```
.clinerules/
  rules.md
  workflows/
    start.md       # Start a new feature from user story
    morning.md     # Daily status check (threads, SonarQube, pipeline)
    eod.md         # Update MR & draft reviewer replies
    commit.md      # Stage, test, commit with conventional message
    close.md       # Post-merge retrospective

memory-bank/
  current-mr.md    # Your project configuration (update this first!)
  handover.md      # Daily progress tracker
  story.md         # Feature plan
  retro.md         # Retrospective after merge

docs/
  quick-reference.md    # Cheat sheet for common tasks
  workflow-examples.md  # Real examples of each workflow
```

## MCP servers used by this project

This project relies on **local MCP (Model Context Protocol) servers** so Cline can interact with enterprise GitLab and SonarQube instances even when an official MCP endpoint is not available/enabled.

### GitLab MCP (local, Python)
- Project: https://github.com/wadew/gitlab-mcp
- Purpose in this kit:
  - read MR discussions/threads (with conversation history)
  - check pipeline status / jobs
  - update MR description (from repo MR template)
  - draft replies to remediated review threads

### SonarQube MCP (local, Python)
- Project: https://github.com/wadew/sonar-mcp
- Purpose in this kit:
  - check quality gate status
  - list bugs/vulnerabilities/code smells
  - read coverage metrics (overall and per-file)

> Notes for enterprise setups: you typically want branch/MR context (not only main branch). This kit’s workflows are written so the agent can use MCP tool schema discovery if your SonarQube parameters differ by installation.

---

## 🚀 Quick Start (5 minutes)

### 1) Clone the repository
```bash
# Clone from your GitLab/GitHub instance
git clone https://gitlab.company.tld/<your-org>/<your-repo>.git
cd <your-repo>
```

### 2) Create and activate a virtual environment (recommended)
```bash
pip install uv
uv venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows (PowerShell)
. .\.venv\Scripts\Activate.ps1
```

### 3) Install MCP servers
```bash
uv pip install gitlab-mcp sonar-mcp
```

### 4) Create API tokens
**GitLab**
- Create a Personal Access Token (PAT)
- Scope: `api`

**SonarQube**
- Create a Sonar token with permission to browse issues/metrics

⚠️ Never commit these tokens.

### 5) Configure MCP servers in Cline
In **Cline → MCP Servers**, add:

**GitLab MCP**
- Command: `gitlab-mcp`
- Environment variables:
  ```text
  GITLAB_URL=https://gitlab.company.tld
  GITLAB_TOKEN=xxxxxxxx
  GITLAB_ALLOWED_PROJECT_IDS=12345
  ```

**SonarQube MCP**
- Command: `sonar-mcp`
- Environment variables:
  ```text
  SONAR_URL=https://sonar.company.tld
  SONAR_TOKEN=xxxxxxxx
  ```

Restart Cline after adding servers.

### 6) Fill project metadata
Edit `memory-bank/current-mr.md`:

```md
base_branch: main
feature_branch: my-feature

project_id: 12345
mr_iid: 67

sonar_project_key: my-project

mr_template_path: .gitlab/merge_request_templates/default.md

precommit_runner: null  # or "lint-staged" | "pre-commit" | "both"
```

### 7) Validate your setup (optional but recommended)
```bash
python validate_mcp_setup.py
```

This checks:
- Project structure
- Memory bank configuration
- MCP package installation
- GitLab/SonarQube environment variables (if running in Cline)

### 8) Run your first workflow
In Cline, run:

```
/morning.md
```

If you see MR thread summaries and quality signals → you're ready.

---

## 💡 How to Use This Kit (Day-to-Day)

### Typical Day with Cline

**Morning (2 minutes):**
```
You: Run the morning.md workflow

Cline: [Shows MR status, reviewer comments, SonarQube results, suggests priorities]
```

**While Coding:**
```
You: Let's implement the password validation function

Cline: [Writes code, creates tests, runs them]

You: Looks good! Run the commit.md workflow

Cline: [Stages changes, runs hooks, proposes commit message, commits if approved]
```

**End of Day (2 minutes):**
```
You: Run the eod.md workflow

Cline: [Updates MR description, drafts replies to reviewer threads, updates handover]
```

**Total time saved per day: 30-60 minutes** ⏰

### Real Example: Your First Conversation

**You:** `Run the morning.md workflow`

**Cline responds:**
```
🔍 Checking MR !67...

GitLab Status:
- Pipeline: ✅ PASSING
- Threads: 2 unresolved

Thread #1: "Can you add error handling here?"
Thread #2: "Missing tests for edge case"

SonarQube: ✅ Quality Gate PASSED
Coverage: 85.2%

Today's priorities:
1. Add error handling (Thread #1)
2. Add edge case tests (Thread #2)

Ready to start with Thread #1?
```

**You:** `Yes, let's fix the error handling`

**Cline:** `[Reads the file, adds try-catch, updates tests, shows you the diff]`

**You:** `Perfect! Run the commit.md workflow`

**See? Easy!** Check [user-guide.md](user-guide.md) for complete walkthroughs.

---

## ✅ MCP validation & troubleshooting

### Quick validation
Run the validation script to check your setup:

```bash
python validate_mcp_setup.py
```

### Manual validation

### Validate GitLab MCP
In Cline:
- Ask it to **list available GitLab MCP tools**
- Then ask it to **fetch MR !<mr_iid> metadata**

If it fails:
- verify `GITLAB_URL`
- PAT scope = `api`
- correct `project_id` and `mr_iid`
- ensure `GITLAB_ALLOWED_PROJECT_IDS` includes your project

### Validate SonarQube MCP
In Cline:
- Ask it to **list available Sonar MCP tools**
- Then ask it to **get quality gate status** for your project (branch/MR context if needed)

If it fails:
- verify `SONAR_URL`
- Sonar token permissions
- confirm your project key exists in SonarQube

---

## Workflows (run in Cline)

Just say **"Run the [workflow-name] workflow"** in Cline:

| Workflow | When to use | What it does |
|----------|-------------|--------------|
| `start.md` | Beginning of feature | Paste Rally story → generates execution plan |
| `morning.md` | Start of day | Shows MR threads, pipeline, SonarQube status, priorities |
| `eod.md` | End of day | Updates MR description, drafts reviewer replies, writes handover |
| `commit.md` | After coding | Stages changes, runs hooks, proposes commit message |
| `close.md` | After MR merges | Creates retrospective comparing plan vs reality |

**Example:** Type `Run the morning.md workflow` in Cline and hit enter! 🚀

📖 **See detailed examples:** [docs/workflow-examples.md](docs/workflow-examples.md)

---

## Contributing / Development workflow (enforced by EOD)

### Commits (Conventional Commits)
This repository uses **semantic-release** to generate changelogs and manage versioning.
Commits must follow **Angular Conventional Commits**:

`<type>(<scope>): <subject>`

Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

### Merge Request overview
MR descriptions must be based on the repository’s **default MR template** and filled out accurately.

### Merge Requests (reviews & threads)
When a thread is remediated, reply with:
- what changed
- where (file/module)
- how to verify (tests/commands)
…and request the reviewer to confirm and resolve the thread.

### Quality gates (tests, coverage, SonarQube)
- All functional changes must include or update automated tests.
- Avoid reducing coverage without justification.
- CI runs SonarQube analysis; new issues introduced by the MR must be fixed and quality gate must pass.

---

## ❓ FAQ & Troubleshooting

### "How do I talk to Cline?"

Just type naturally in the Cline chat window:
- ✅ "Run the morning.md workflow"
- ✅ "Show me unresolved MR threads"
- ✅ "Help me fix the SonarQube bug"
- ✅ "Let's implement the password validator"

### "What if Cline doesn't understand me?"

Be more specific:
- ❌ "Fix it" → ✅ "Fix the null pointer bug in AuthService.ts line 45"
- ❌ "Update MR" → ✅ "Run the eod.md workflow"

### "Cline can't see my MR threads"

1. Run `python validate_mcp_setup.py`
2. Check `memory-bank/current-mr.md`:
   - Is `project_id` correct?
   - Is `mr_iid` correct?
3. Verify GitLab MCP in Cline settings:
   - `GITLAB_TOKEN` has `api` scope
   - `GITLAB_ALLOWED_PROJECT_IDS` includes your project

### "SonarQube data isn't showing"

1. Run `python validate_mcp_setup.py`
2. Check SonarQube MCP configuration:
   - `SONAR_URL` correct?
   - `SONAR_TOKEN` valid?
3. Verify `sonar_project_key` in `memory-bank/current-mr.md`

### "Pre-commit hooks aren't running"

Edit `memory-bank/current-mr.md` and set:
```yaml
precommit_runner: "lint-staged"  # or "pre-commit" or "both"
```

### "I made a mistake, how do I undo?"

Just tell Cline:
```
Undo that last change
```

Or use git:
```
git restore <filename>
```

### "Where can I learn more?"

- **[User Guide](user-guide.md)** - Complete walkthrough with examples
- **[Quick Reference](docs/quick-reference.md)** - Cheat sheet
- **[Workflow Examples](docs/workflow-examples.md)** - Real scenario examples

### "Can I customize the workflows?"

**Yes!** Workflows are just markdown files in `.clinerules/workflows/`. Edit them to match your team's process.

### "What if I'm stuck?"

Ask Cline:
```
I'm stuck. Can you explain what I should do next?
```

Cline can explain itself and help you get unstuck!

---

## 📦 Public GitHub release checklist

### Documentation
- [ ] README includes Quick Start + MCP setup + workflow overview + beginner section
- [ ] User guide with step-by-step examples (`user-guide.md`)
- [ ] Quick reference cheat sheet (`docs/quick-reference.md`)
- [ ] Workflow examples with real scenarios (`docs/workflow-examples.md`)
- [ ] No internal URLs or tokens
- [ ] Enterprise assumptions are clear
- [ ] FAQ/Troubleshooting section complete

### Repository hygiene
- [ ] `.clinerules/` committed
- [ ] `memory-bank/` committed with templates only (with configuration markers)
- [ ] `.gitlab/merge_request_templates/` committed
- [ ] `.gitignore` covers `.venv/`, `.env`, etc.
- [ ] `validate_mcp_setup.py` script included

### Workflow sanity
- [ ] `/start.md` works with pasted story
- [ ] `/morning.md` runs without modifying files
- [ ] `/eod.md` updates MR description and creates thread reply drafts
- [ ] `/commit.md` requires explicit approval
- [ ] `validate_mcp_setup.py` runs successfully

### Security
- [ ] Tokens are environment-only
- [ ] GitLab MCP uses project allowlist
- [ ] Sonar MCP token is least-privilege (read where possible)

### Licensing
- [ ] Add a `LICENSE` file (MIT/Apache-2.0 recommended)
- [ ] Verify MCP server licenses are compatible

---

## 🤝 Getting Help & Contributing

### New to this?
Start with [user-guide.md](user-guide.md) - it walks you through everything step-by-step!

### Quick help
- **[Quick Reference](docs/quick-reference.md)** - Cheat sheet for common tasks
- **[Workflow Examples](docs/workflow-examples.md)** - See real examples
- **[FAQ](#-faq--troubleshooting)** - Common questions answered

### Contributing
Contributions welcome! This is an open-source template designed to be customized. Feel free to:
- Add new workflows for your team's processes
- Improve documentation with your learnings
- Share your customizations via PRs
- Report issues or suggest improvements

### Questions?
**Just ask Cline!** Seriously:
```
Can you explain how this workflow kit works?
```

Cline can read all these docs and explain them to you! 🤖
