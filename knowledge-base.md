# Cline — AI Coding Agent
**Developer Knowledge Base**

> Integrates: **GitLab MCP** · **SonarQube MCP** · **OpenAI-compatible LLMs**
> Workflow kit: [github.com/siwardean/cline-workflow](https://github.com/siwardean/cline-workflow)

---

## PART A — INSTALL & SETUP

### Prerequisites

| Requirement | Details |
|---|---|
| **VS Code Server** | Already running in your environment · Access via browser |
| **Python + uv** | `pip install uv` |
| **python-gitlab-mcp** | `uv pip install python-gitlab-mcp` (GitLab MCP server) |
| **sonar-mcp** | `uv pip install sonar-mcp` (SonarQube MCP server) |
| **GitLab token** | Scope: `api` · GitLab → Settings → Access Tokens · Get from team lead |
| **SonarQube token** | SonarQube → My Account → Security · Get from team lead |
| **LLM API access** | Bank's OpenAI-compatible endpoint + API key · Never commit |
| **Git + GitLab** | Git configured with your credentials |
| **IT / admin rights** | Request if IT-managed before installing anything |

---

### A1 — Install Cline Extension

1. In the VS Code Server interface, click the **Extensions** icon in the Activity Bar (or press `Ctrl+Shift+X`)
2. Search **Cline** → select the extension by **saoudrizwan** (`saoudrizwan.claude-dev`) → **Install**
3. Click the Cline icon that appears in the Activity Bar to open the panel
4. Drag Cline to the right sidebar (keeps the file explorer on the left)

> 💡 **VS Code Server tip:** If the Cline panel doesn't open, use Command Palette (`Ctrl+Shift+P`) → `Cline: Open In New Tab`

---

### A2 — Configure the LLM Provider

Cline panel → **gear icon** → provider → select **OpenAI Compatible**

Enter the following (all from your team lead):
- **Base URL** — bank's internal OpenAI-compatible endpoint
- **API key** — your personal key
- **Model name** — as specified by the team

Send `Hello?` to verify the connection — you should see a response and a token cost counter.

> ⚠️ Never paste credentials in chat. Never commit API keys to git.

---

### A3 — Install & Configure MCP Servers

MCP (Model Context Protocol) servers let Cline communicate directly with GitLab and SonarQube.

**Install the servers** in a terminal:

```bash
pip install uv
uv pip install python-gitlab-mcp sonar-mcp
```

**Register them in Cline:** Cline panel → gear → **MCP Servers** tab → add:

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "python-gitlab-mcp",
      "env": {
        "GITLAB_URL": "https://gitlab.your-bank.tld",
        "GITLAB_TOKEN": "your-gitlab-token",
        "GITLAB_ALLOWED_PROJECT_IDS": "12345"
      }
    },
    "sonarqube": {
      "command": "sonar-mcp",
      "env": {
        "SONAR_URL": "https://sonar.your-bank.tld",
        "SONAR_TOKEN": "your-sonarqube-token"
      }
    }
  }
}
```

> ⚠️ **Never commit tokens.** `cline_mcp_settings.json` is git-ignored by default.

**Verify the setup** by asking Cline in chat:
- *"List tools from the gitlab MCP server"* → should return a list of tools
- *"List tools from the sonarqube MCP server"* → should return a list of tools

Or run the validation script if you have the workflow kit installed:
```bash
python validate_mcp_setup.py
```

---

### A4 — Validation Checklist

- [ ] Cline panel opens without errors
- [ ] Test message works — cost counter visible
- [ ] GitLab MCP tools listed in response to chat question
- [ ] SonarQube MCP tools listed in response to chat question
- [ ] Git configured (`git config user.name` and `git config user.email` return your details)

---

## PART B — HOW TO USE

### B1 · Using Cline — The Basics

Cline is a chat panel inside VS Code Server. You type in plain language; it reads your codebase, proposes changes, and waits for your review before applying anything. No special syntax required — just describe what you want.

#### The Two Modes

| Mode | What it does |
|---|---|
| 🧠 **Plan mode** | Cline reads and explores — no files are touched. Safe for understanding the codebase, planning an approach, asking questions. |
| ⚡ **Act mode** | Cline proposes and applies changes — files, terminal commands, edits. Each action shows a diff you must approve before it executes. |

#### The Recommended Workflow for Every Feature

For any new feature or significant change, **always start in Plan mode and only switch to Act once the plan fully matches what you need**. This is the single most effective habit for saving tokens, avoiding rework, and preventing rollbacks.

| Step | What to do |
|---|---|
| **1 · Start in Plan mode** | Describe the feature to implement. Cline reads the codebase, identifies relevant files, and proposes a step-by-step plan — without touching anything. |
| **2 · Refine the plan** | Stay in Plan mode. Ask Cline to adjust scope, split tasks, reconsider the approach, or explain trade-offs. Iterate freely — no cost from file edits or rollbacks. |
| **3 · Confirm the plan** | Only switch to Act mode once the plan fully matches what you need. At this point both you and Cline have a shared, agreed understanding of what will be built. |
| **4 · Execute in Act mode** | Cline applies changes one step at a time. Review each diff, approve what looks right, and redirect if needed. The agreed plan minimises surprises. |

> 💡 **Why this matters:** Every file edit Cline applies in Act mode that later needs undoing costs tokens twice — once to write it, once to fix it. Refining the plan in Plan mode costs almost nothing by comparison. A good plan upfront is the most token-efficient thing you can do.

#### How to Talk to Cline

Cline understands natural language. A few patterns that work well:

| Pattern | Example |
|---|---|
| **Describe the goal** | *"Add input validation to the registration form"* |
| **Point to a file** | *"In src/auth/AuthService.ts, the login method doesn't handle expired tokens"* |
| **Ask questions first** | *"What does the UserService class do?"* — use Plan mode to understand before changing anything |
| **Iterate with feedback** | *"Good, but also validate the email format"* — each reply refines without starting over |
| **Ask for explanations** | *"Why did you choose this approach?"* — Cline reasons through decisions |
| **Undo or course-correct** | *"Undo that last change"* or *"Let's try a different approach"* |

#### Reviewing Changes

Every file edit appears as a diff. You can: **Approve** (apply), **Reject** (discard + explain), **edit manually** after accepting, or ask Cline to revise before applying.

> ⚠️ **Read every diff before approving.** Cline is helpful but not infallible — you are the senior developer.

#### Terminal Commands

When Cline needs to run a command it shows it first and asks permission. Output is streamed in real time. Anything destructive is flagged explicitly.

#### Cost & Token Awareness

The panel shows a running token count per session. Keep prompts focused on one task, use Plan mode for exploration, and start a new session for a new task.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Cline panel not opening | Command Palette (`Ctrl+Shift+P`) → `Cline: Open In New Tab` |
| API connection error | Check Base URL + API key · Confirm VPN is active · Check VS Code Server proxy settings |
| MCP servers not found | `python-gitlab-mcp --version` · if error: `uv pip install --upgrade python-gitlab-mcp sonar-mcp` |
| Can't access GitLab MR | Check `GITLAB_TOKEN` has `api` scope · Verify `GITLAB_URL` is reachable |
| SonarQube data missing | Check `SONAR_URL` + `SONAR_TOKEN` · Confirm `sonar_project_key` matches your project |
| High token cost | Smaller prompts · Plan mode before Act |
| Unexpected file edits | Use Plan mode · Review every diff · `git restore <file>` to undo |

> 🆘 **Support**: Team lead → API keys · IT → proxy/admin · Tribe Slack → Cline questions

---

## PART C — OPTIONAL: Workflow Automation Kit

> This section describes an optional workflow kit that automates the full GitLab feature lifecycle. It is not required to use Cline, but significantly reduces manual steps.
>
> Kit: [github.com/siwardean/cline-workflow](https://github.com/siwardean/cline-workflow)

### What the Kit Adds

Five pre-written workflow files that Cline can invoke with a `/` command. They connect Cline to GitLab and SonarQube so status checks, MR updates, commit messages, code reviews, and retrospectives happen automatically.

| Who | Does what |
|---|---|
| **YOU** | Approve commits, merge MRs, post GitLab replies |
| **CLINE** | Status checks, MR updates, commit messages, code reviews, retrospectives |
| **TOGETHER** | Pair programming — you describe, Cline implements, you review |

---

### C1 — Installation

```bash
git clone https://github.com/siwardean/cline-workflow.git && cd cline-workflow
python install.py      # interactive installer: MCP servers + workflow files
```

Or manually copy the workflow files:

```bash
mkdir -p ~/Documents/Cline/Rules && mkdir -p ~/Documents/Cline/Workflows
cp .clinerules/rules.md ~/Documents/Cline/Rules/
cp .clinerules/workflows/* ~/Documents/Cline/Workflows/
```

Type `/` in Cline chat — all 5 workflows should appear in autocomplete.

> 💡 **Project-specific alternative**: copy `.clinerules/` into your project root and commit — team gets same workflows on clone. Project rules override global.

---

### C2 — Configure Your Project (memory-bank)

Create `memory-bank/current-mr.md` in your project root — every workflow reads this file:

```yaml
base_branch: main
project_id: 12345

merge_requests:                    # supports multiple MRs
  - mr_iid: 67
    feature_branch: feature/my-feature
    description: "My feature"

sonar_project_key: my-project
mr_template_path: .gitlab/merge_request_templates/default_merge_request.md
precommit_runner: null             # null | lint-staged | pre-commit | both
```

---

### C3 — The Five Workflows

#### /start.md — Feature Planning + Branch + MR

**When:** Beginning of every feature.

**Flow:** Reads story → greps codebase → generates 5–12 task plan → presents for your review → on approval: creates branch + GitLab MR automatically, writes `memory-bank/story.md`

**Input:** Paste your story in chat:
```
Story title: <short title>
Description: <what and why>
Acceptance criteria:
  1. ...
```

**Output:** Feature branch (pushed) · GitLab MR (Draft) · `memory-bank/story.md`

---

#### /morning.md — Daily Ritual (Wrap Up + Status)

**When:** Every morning. No input needed.

**Phase 1 — Wrap up yesterday:**
Updates all MR descriptions on GitLab · Drafts thread replies · Writes `memory-bank/handover.md`

**Phase 2 — Start today:**
Fetches live GitLab + SonarQube status · Prioritises tasks · Delivers full daily report

**Output:** Updated MR descriptions · Draft thread replies (copy to GitLab) · `memory-bank/handover.md`

---

#### /commit.md — Commit Helper

**When:** After making code changes.

**Flow:** Auto-stages → runs hooks → auto-fixes lint → proposes one commit message → **single approval gate** → commits + pushes + updates MR description

**Output:** Committed + pushed + MR progress block updated

---

#### /code-reviewer.md — MR Code Review

**When:** When asked to review an MR.

**Flow:** Fetches diff + threads → assesses existing threads → reviews code (Bug · Security · Perf · Style · Tests · Docs) → shows findings table → **you pick which to post** → creates GitLab discussion threads

**Output:** GitLab discussion threads posted + summary

---

#### /close.md — Post-Merge Retrospective

**When:** After your MR is merged in GitLab.

**Flow:** Reads original plan → fetches merged MR data → evaluates each AC → compares plan vs reality → calculates time variance → writes `memory-bank/retro.md`

**Output:** `memory-bank/retro.md`

---

### C4 — The Memory Bank

Cline has no built-in memory between sessions. The `memory-bank/` folder is the persistent context shared across workflows.

> ⚠️ `story.md`, `handover.md`, and `retro.md` are **gitignored** — local AI state, never committed. `current-mr.md` is committed (project config).

| File | Contains | Updated by | When |
|---|---|---|---|
| `current-mr.md` | project_id, MR list, SonarQube key, hooks config | **YOU** + `/start.md` | Starting a new MR |
| `story.md` | Tasks mapped to ACs, files, tests, SonarQube risks | `/start.md` | Beginning of feature |
| `handover.md` | Commits, current state, blockers, thread drafts | `/morning.md` | Every morning |
| `retro.md` | AC compliance, estimate variance, lessons learned | `/close.md` | After MR merged |

---

### C5 — Workflow Cheat Sheet

| Workflow | When | Output |
|---|---|---|
| `/start.md` | Beginning of feature | Branch + MR created · `memory-bank/story.md` |
| `/morning.md` | Start of workday | Updated MR descriptions + draft replies + status report |
| `/commit.md` | After code changes | Committed + pushed + MR progress updated |
| `/code-reviewer.md` | When reviewing an MR | GitLab discussion threads posted |
| `/close.md` | After MR merged | `memory-bank/retro.md` |

---

### C6 — Workflow Troubleshooting

| Symptom | Fix |
|---|---|
| Workflows not in `/` menu | Files need `.md` extension in `~/Documents/Cline/Workflows/` · Restart VS Code Server |
| Can't access GitLab MR | Run `python validate_mcp_setup.py` · Check `project_id` + `mr_iid` |
| Hooks not running | Set `precommit_runner` in `current-mr.md`: `lint-staged` / `pre-commit` / `both` / `null` |
| `story.md` missing | Paste story details manually in chat when running `/close.md` |
| Branch/MR not created | `/start.md` creates them on plan approval — ensure GitLab MCP is reachable |

---

### Links

- Workflow kit: [github.com/siwardean/cline-workflow](https://github.com/siwardean/cline-workflow)
- Community workflows: [github.com/cline/prompts](https://github.com/cline/prompts)
- Cline docs: [docs.cline.bot](https://docs.cline.bot)
- GitLab MCP: [github.com/wadew/gitlab-mcp](https://github.com/wadew/gitlab-mcp)
- SonarQube MCP: [github.com/wadew/sonar-mcp](https://github.com/wadew/sonar-mcp)
- GitLab Wiki (this KB): *[ your GitLab Wiki URL ]*

---
