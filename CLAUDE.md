# Workspace Rules

## Tool-first behavior
- **Always use tools before reading files** — MCP tools and terminal commands first
- **Minimize context usage** — don't read large files unless necessary
- **Parallel tool calls** — fetch MCP data in parallel when possible
- **Verify before acting** — check file existence, MCP availability

## Tool usage (Claude Code)
- Read files: `Read` tool
- Write/edit files: `Write` / `Edit` tools
- Run commands: `Bash` tool
- MCP tools: available via connected MCP servers

## MCP tools
- **GitLab MCP**: use explicit tool names (e.g., `gitlab_get_merge_request`, `gitlab_get_discussions`, `gitlab_update_merge_request`)
- **SonarQube MCP**: use explicit tool names (e.g., `sonar_get_quality_gate`, `sonar_get_issues`)
- **Always handle MCP failures gracefully** — provide user-friendly error messages
- **Validate MCP responses** — check for empty/null data

## Error handling
- If MCP server unavailable: inform user, suggest `python validate_mcp_setup.py`
- If file not found: inform user, suggest checking `memory-bank/current-mr.md`
- If git command fails: show error, suggest remediation
- Never fail silently — always explain what went wrong

## Source of truth
- MR overview MUST follow the repo MR template (`.gitlab/merge_request_templates/default.md`)
- MR configuration in `memory-bank/current-mr.md` is authoritative
- Story plan in `memory-bank/story.md` defines scope

## Code quality
- **Clean Code principles required** — readable, maintainable, self-documenting
- **Tests mandatory** — all functional changes need tests
- **Coverage targets** — maintain or improve coverage
- **No skipping quality checks** — address SonarQube issues before merge

## SonarQube mandatory retrieval
When workflows invoke SonarQube checks, Claude MUST retrieve:
- Quality Gate status (pass/fail + reason)
- Bugs (count + severity + locations)
- Vulnerabilities (count + severity + locations)
- Code Smells (count + severity + locations)
- Coverage (overall % + diff vs base)

Results MUST drive planning and remediation priority.

## Branch naming
- **Format**: `feature/<keyword>_<keyword>_<keyword>`
- Extract 2–4 meaningful keywords from the story title and description
- **Avoid generic words**: add, update, fix, feature, implement, new, change
- Lowercase, underscores only, no special characters, no ticket numbers
- Keep short: 2–4 keywords max

Examples:
- "Allow users to reset their password via email" → `feature/password_reset_email`
- "Add pagination to the product listing page" → `feature/product_listing_pagination`
- "Integrate Stripe for subscription billing" → `feature/stripe_subscription_billing`

## Commits
- **Angular Conventional Commits required** — `<type>(<scope>): <subject>`
- **Types**: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- **Scope**: feature or component name (not file type)
- **Subject**: imperative mood, no period, <50 chars
- **Body**: explain what and why (not how)
- **Footer**: BREAKING CHANGE if API changed

## Workflow execution
- **Show progress** — tell user what's happening at each step
- **Require approval** — for commits, destructive operations, MR updates
- **Summarize results** — don't just execute, explain outcomes
- **Provide next steps** — guide user on what to do next
