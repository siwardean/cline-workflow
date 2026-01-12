# 🎯 Quick Reference Guide

Quick answers for common tasks. Keep this handy!

---

## 🗣️ How to Run Workflows

| What you say | What happens |
|--------------|--------------|
| `Run the morning.md workflow` | Checks MR threads, pipeline, SonarQube status |
| `Run the eod.md workflow` | Updates MR description, drafts thread replies |
| `Run the commit.md workflow` | Stages changes, runs hooks, proposes commit message |
| `Run the start.md workflow` | Creates execution plan from user story |
| `Run the close.md workflow` | Writes retrospective after MR merge |

---

## 💬 Common Things to Say to Cline

### Starting Your Day
```
Run the morning.md workflow
```

### Before Leaving
```
Run the eod.md workflow
```

### Committing Code
```
Run the commit.md workflow
```

### Checking Status
```
What's my current status?
Show me unresolved MR threads
What's blocking the SonarQube quality gate?
```

### Working on Code
```
Let's implement the password validation function
Help me fix the bug in UserService.ts line 45
Can you refactor this function to be more readable?
Add tests for the login functionality
```

### Understanding the Codebase
```
Where do we handle user authentication?
Show me all the API endpoints
What does the AuthService class do?
```

### Getting Help
```
Explain what this code does
Why is SonarQube failing?
What should I work on next?
Can you show me an example of a good commit message?
```

---

## 📂 Important Files

| File | Purpose | When to Update |
|------|---------|----------------|
| `memory-bank/current-mr.md` | Your MR configuration | When starting a new MR |
| `memory-bank/story.md` | Your feature plan | Auto-updated by `/start.md` |
| `memory-bank/handover.md` | Daily progress tracker | Auto-updated by `/eod.md` |
| `.clinerules/rules.md` | Coding standards | When team standards change |

---

## 🔧 Quick Fixes

### "Cline can't see my MR"
1. Open `memory-bank/current-mr.md`
2. Update `project_id` and `mr_iid`
3. Save and try again

### "SonarQube isn't working"
```
python validate_mcp_setup.py
```
Check if SONAR_URL and SONAR_TOKEN are configured in Cline MCP settings.

### "Git hooks aren't running"
1. Open `memory-bank/current-mr.md`
2. Set `precommit_runner: "lint-staged"` (or your hook type)
3. Run commit workflow again

### "I made a mistake"
```
Undo that last change
```
or
```
git restore <filename>
```

---

## 🎓 Workflow Cheat Sheet

### Start Feature (/start.md)
**Input:** Paste your user story  
**Output:** Execution plan in `memory-bank/story.md`  
**When:** Beginning of a new feature

### Morning Check (/morning.md)
**Input:** Nothing needed  
**Output:** Status update, prioritized task list  
**When:** Start of workday

### End of Day (/eod.md)
**Input:** Nothing needed  
**Output:** Updated MR, draft replies, handover  
**When:** Before you leave

### Commit (/commit.md)
**Input:** Staged/unstaged changes  
**Output:** Clean commit with conventional message  
**When:** After implementing something

### Close Feature (/close.md)
**Input:** Merged MR  
**Output:** Retrospective in `memory-bank/retro.md`  
**When:** After MR is merged

---

## 🚨 Red Flags

| If Cline says... | You should... |
|------------------|---------------|
| "I can't access the MR" | Check GitLab MCP configuration |
| "SonarQube returned an error" | Check SONAR_TOKEN and project_key |
| "No changes staged" | Stage your changes or ask Cline to stage them |
| "Quality gate failed" | Ask "What's blocking the quality gate?" |

---

## 💡 Pro Tips

1. **Use workflows daily** - They save time and ensure consistency
2. **Update current-mr.md** - Keep it accurate for best results
3. **Review before approving** - Cline is helpful but not perfect
4. **Ask questions** - Cline can explain anything
5. **Customize workflows** - Edit them to fit your team's process

---

## 📱 Quick Validation

Run this anytime to check your setup:
```bash
python validate_mcp_setup.py
```

---

## 🆘 Getting Unstuck

**Cline seems confused?**
```
Let's start over. Here's what I want to do: [explain clearly]
```

**Not sure what to do next?**
```
Based on my story.md and current status, what should I work on next?
```

**Want to understand something?**
```
Explain this like I'm new to the codebase
```

---

**Keep this page bookmarked for quick reference!** 🔖

