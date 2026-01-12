# Workspace Rules (Cline)

## Tool-first behavior
- **Always use tools before reading files** - MCP tools and terminal commands first
- **Minimize context usage** - Don't read large files unless necessary
- **Parallel tool calls** - Fetch MCP data in parallel when possible
- **Verify before acting** - Check file existence, MCP availability

## Tool usage guidelines
### File operations
- Use `read_file` with specific paths, not wildcards
- Use `write` (not `write_file`) for creating/updating files
- Use `search_replace` for targeted edits
- Use `list_dir` to discover structure before reading

### Terminal commands
- Use `run_terminal_cmd` (not `execute_command`)
- Always check exit codes
- Capture output for validation
- Use `--` to separate flags from arguments in git commands

### MCP tools
- **GitLab MCP**: Use explicit tool names (e.g., `gitlab_get_merge_request`, `gitlab_get_discussions`)
- **SonarQube MCP**: Use explicit tool names (e.g., `sonar_get_quality_gate`, `sonar_get_issues`)
- **Always handle MCP failures gracefully** - Provide user-friendly error messages
- **Validate MCP responses** - Check for empty/null data

## Error handling
- If MCP server unavailable: inform user, suggest `python validate_mcp_setup.py`
- If file not found: inform user, suggest checking `memory-bank/current-mr.md`
- If git command fails: show error, suggest remediation
- Never fail silently - always explain what went wrong

## Source of truth
- MR overview MUST follow the repo MR template (`.gitlab/merge_request_templates/default.md`)
- MR configuration in `memory-bank/current-mr.md` is authoritative
- Story plan in `memory-bank/story.md` defines scope

## Code quality
- **Clean Code principles required** - readable, maintainable, self-documenting
- **Tests mandatory** - all functional changes need tests
- **Coverage targets** - maintain or improve coverage
- **No skipping quality checks** - address SonarQube issues before merge

## SonarQube mandatory retrieval
When workflows invoke SonarQube checks, agents MUST retrieve:
- Quality Gate status (pass/fail + reason)
- Bugs (count + severity + locations)
- Vulnerabilities (count + severity + locations)
- Code Smells (count + severity + locations)
- Coverage (overall % + diff vs base)

Results MUST drive planning and remediation priority.

## Commits
- **Angular Conventional Commits required** - `<type>(<scope>): <subject>`
- **Types**: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- **Scope**: feature or component name (not file type)
- **Subject**: imperative mood, no period, <50 chars
- **Body**: explain what and why (not how)
- **Footer**: BREAKING CHANGE if API changed

## Workflow execution
- **Show progress** - Tell user what's happening at each step
- **Require approval** - For commits, destructive operations, MR updates
- **Summarize results** - Don't just execute, explain outcomes
- **Provide next steps** - Guide user on what to do next
