# 📚 Workflow Examples: Real Scenarios

See exactly what each workflow does with real examples.

---

## Table of Contents

1. [Start Workflow Examples](#start-workflow-examples)
2. [Morning Workflow Examples](#morning-workflow-examples)
3. [EOD Workflow Examples](#eod-workflow-examples)
4. [Commit Workflow Examples](#commit-workflow-examples)
5. [Close Workflow Examples](#close-workflow-examples)

---

## Start Workflow Examples

### Example 1: Simple Feature

**You say:**
```
Run the start.md workflow. Here's my story:

Title: Add forgot password link
Description: Users need a way to reset their password
Acceptance Criteria:
  1) Show "Forgot Password?" link on login page
  2) Link navigates to password reset page
  3) Page shows instructions
Estimate: 0.5 man-days
```

**Cline produces:**
```
📋 Execution Plan for: Add forgot password link

Task 1: Add password reset route
- Files: src/routes/index.ts
- Tests: routes.test.ts
- AC: [2]
- DoD: Route renders PasswordResetPage

Task 2: Create password reset page component
- Files: src/pages/PasswordResetPage.tsx
- Tests: PasswordResetPage.test.tsx
- AC: [3]
- DoD: Page displays instructions, form exists

Task 3: Add link to login page
- Files: src/pages/LoginPage.tsx
- Tests: LoginPage.test.tsx
- AC: [1]
- DoD: Link visible and clickable

Task 4: Update documentation
- Files: README.md
- DoD: Usage documented

✅ AC Coverage:
- AC1 → Task 3
- AC2 → Task 1, Task 2
- AC3 → Task 2

📝 Saved to: memory-bank/story.md
```

---

### Example 2: Complex Feature

**You say:**
```
Run the start.md workflow. Here's my story:

Title: Implement two-factor authentication
Description: Add 2FA for enhanced security
Notes: Use TOTP (Time-based One-Time Password)
Acceptance Criteria:
  1) Users can enable 2FA in settings
  2) QR code generated for authenticator apps
  3) Backup codes provided (10 single-use codes)
  4) 2FA required on login if enabled
  5) Admin can require 2FA for all users
Estimate: 5 man-days
```

**Cline produces:**
```
📋 Execution Plan for: Implement two-factor authentication

Task 1: Add 2FA database schema
- Files: migrations/XXXX-add-2fa-fields.ts
- Tests: migration.test.ts
- AC: [1]
- SonarQube risks: Schema review needed

Task 2: Implement TOTP generation service
- Files: src/services/TotpService.ts
- Tests: TotpService.test.ts
- AC: [2]
- SonarQube risks: Security review (cryptography)

Task 3: Create backup codes generator
- Files: src/services/BackupCodesService.ts
- Tests: BackupCodesService.test.ts
- AC: [3]
- SonarQube risks: Secure random generation

Task 4: Build 2FA settings UI
- Files: src/components/TwoFactorSettings.tsx
- Tests: TwoFactorSettings.test.tsx
- AC: [1, 2, 3]

Task 5: Update authentication flow
- Files: src/services/AuthService.ts, src/middleware/auth.ts
- Tests: auth-flow.test.ts
- AC: [4]
- SonarQube risks: Complexity increase

Task 6: Add admin 2FA policy controls
- Files: src/pages/AdminSettingsPage.tsx
- Tests: AdminSettingsPage.test.tsx
- AC: [5]

Task 7: Update API documentation
- Files: README.md
- AC: All

⚠️ Open Questions:
- Which TOTP library should we use?
- How long should backup codes be valid?
- Should we support SMS 2FA in the future?

🔒 Security Considerations:
- TOTP secrets must be encrypted at rest
- Backup codes must be hashed
- Rate limiting on 2FA attempts
- Audit logging for 2FA events
```

---

## Morning Workflow Examples

### Example 1: Everything is Good

**You say:**
```
Run the morning.md workflow
```

**Cline shows:**
```
🌅 Good Morning! Status for MR !156

📋 GitLab Status:
- Branch: feature/add-pagination
- Base: main
- Pipeline: ✅ PASSING (#2341)
- Last updated: 2 hours ago

💬 MR Threads: All resolved! ✅

📊 SonarQube Status:
✅ Quality Gate: PASSED

Coverage: 91.2% (+0.5% vs main)
Bugs: 0
Vulnerabilities: 0
Code Smells: 0

🎯 Today's Plan:
✅ All acceptance criteria met
✅ All quality checks passing
📝 Ready for final review

Suggested actions:
1. Request final review from team
2. Prepare demo if needed
3. Start next story?
```

---

### Example 2: Issues to Address

**You say:**
```
Run the morning.md workflow
```

**Cline shows:**
```
🌅 Morning Status for MR !145

📋 GitLab Status:
- Branch: feature/user-export
- Base: main
- Pipeline: ❌ FAILED (#2298)
  - Failed job: "test-integration"

💬 MR Threads (3 unresolved):

📌 Thread #1 - src/services/ExportService.ts:67
   @sarah.jones (2 hours ago)
   "This could timeout for large datasets. Consider streaming the response?"
   
📌 Thread #2 - src/api/export.controller.ts:23
   @mike.chen (5 hours ago)
   "Missing rate limiting. Users could abuse this endpoint."
   
📌 Thread #3 - README.md:145
   @sarah.jones (Yesterday)
   "Can you add an example of the export API call?"

📊 SonarQube Status:
❌ Quality Gate: FAILED

Issues blocking merge:
1. 🐛 Bug (High): Potential memory leak in ExportService.ts:89
   "ResultSet not closed in finally block"
   
2. 🔒 Vulnerability (Medium): export.controller.ts:45
   "Path traversal risk - user input not sanitized"
   
3. 💭 Code Smell (Major): ExportService.ts:50-120
   "Cognitive complexity 25 (threshold: 15)"

Coverage: 73.1% (-3.2% vs main) ⚠️

🎯 Priority Plan for Today:

High Priority:
1. Fix memory leak (Bug #1) - blocks merge
2. Fix path traversal (Vulnerability #1) - security issue
3. Fix failing integration test

Medium Priority:
4. Add rate limiting (Thread #2)
5. Refactor ExportService complexity (Code Smell #1)
6. Consider streaming for large datasets (Thread #1)

Low Priority:
7. Add API example to README (Thread #3)
8. Improve test coverage back to 76%+

⏱️ Estimated effort: 4-6 hours

Would you like to start with the memory leak fix?
```

---

## EOD Workflow Examples

### Example 1: Good Progress Day

**You say:**
```
Run the eod.md workflow
```

**Cline does:**
```
🌆 End of Day Update for MR !145

📊 Fetching latest SonarQube results...
✅ Quality Gate: PASSED (previously FAILED)

📝 Updating MR description...

✅ MR Description Updated

## Summary
Export user data to CSV format with pagination support

**User Story:** US-4567

Implemented secure CSV export functionality for user data with proper
rate limiting and streaming for large datasets.

## Proposed changes
- Added ExportService with streaming support
- Implemented rate limiting on export endpoints
- Added path traversal protection
- Refactored complex methods for better maintainability

## Risk and limitations
**Risks:** None remaining
**Limitations:** Export limited to 10,000 records per request
**Mitigation:** Pagination support for larger exports

## How to test
1. POST /api/users/export with valid auth token
2. Verify CSV downloads correctly
3. Try with >1000 users to test streaming
4. Verify rate limit (5 requests per minute)

## Proof
✅ Unit tests: 45 new tests added
✅ Integration tests: All passing
✅ SonarQube: Quality gate PASSED
✅ Coverage: 89.2% (+16.1% improvement)
✅ Pipeline: PASSING (#2301)

---

💬 Drafting replies to resolved threads...

✅ Draft for Thread #1 (Sarah - streaming):
"Great catch! I've refactored to use streaming for datasets >500 records.

Changes:
- ExportService now uses Node.js streams
- Memory usage reduced by ~80% for large exports
- Added tests with 5000 record dataset

Tests: `npm test ExportService.streaming`
Proof: See commit abc123f, pipeline #2301

Can you verify this addresses your concern?"

---

✅ Draft for Thread #2 (Mike - rate limiting):
"Added rate limiting using express-rate-limit middleware.

Changes:
- Rate limit: 5 requests per minute per user
- 429 status with retry-after header
- Redis-backed for distributed systems
- Admin endpoints excluded

Tests: `npm test rate-limiting.spec.ts`
Proof: All tests passing

Please confirm this meets security requirements."

---

✅ Draft for Thread #3 (Sarah - documentation):
"Added comprehensive example to README section 'Exporting Data'.

Changes:
- cURL example
- JavaScript example
- Response format documented
- Error codes explained

Location: README.md lines 234-267"

---

📄 Updating handover...

✅ Handover Updated (memory-bank/handover.md)

# Handover (2026-01-12)

date: 2026-01-12
branch: feature/user-export
base: main
last_checkpoint_commit: abc123f

## What changed today
- Fixed memory leak in ExportService
- Fixed path traversal vulnerability
- Added streaming for large exports
- Implemented rate limiting
- Refactored complex methods
- Improved test coverage to 89.2%

## Current state
✅ Implemented: All core functionality
✅ Implemented: Security fixes
✅ Implemented: Documentation
✅ Completed: All acceptance criteria

## Tests / CI
✅ All tests passing (312 tests, 45 new)
✅ Pipeline: PASSING (#2301)
✅ SonarQube: Quality Gate PASSED
✅ Coverage: 89.2%

## Risks / blockers
None! Ready for review.

## Suggested next steps
1. Copy draft replies to GitLab threads
2. Request final review from Sarah and Mike
3. Monitor for reviewer responses

## Open MR threads (summary)
3 threads addressed with draft replies ready to post

---

🎉 Summary:
✅ MR description updated
✅ 3 draft replies prepared
✅ Handover documented
✅ Quality gate: PASSING

Next: Copy the draft replies above to your GitLab threads!
```

---

### Example 2: Work in Progress

**You say:**
```
Run the eod.md workflow
```

**Cline shows:**
```
🌆 End of Day Update for MR !167

📊 Fetching latest SonarQube results...
⚠️ Quality Gate: FAILED

Issues:
- Coverage: 67.3% (threshold: 75%)
- 1 Bug: Null pointer risk

📝 Updating MR description...

## Summary
Add real-time notifications [IN PROGRESS]

## Proof
⚠️ SonarQube: Quality gate FAILING
- Bug: Fix null pointer in NotificationService.ts:45
- Coverage: Need 8% more coverage

🚧 Work in Progress

---

📄 Updating handover...

# Handover (2026-01-12)

## Current state
✅ Implemented: WebSocket connection setup
✅ Implemented: Notification component UI
🔄 In progress: Service layer error handling
📋 Not started: Integration tests

## Risks / blockers
❌ Quality gate failing (coverage + bug)

## Suggested next steps
1. Fix null pointer bug (15 min)
2. Add integration tests (1-2 hours)
3. Re-run SonarQube scan

---

⚠️ MR is not ready for final review yet.
Focus tomorrow: tests and quality gate.
```

---

## Commit Workflow Examples

### Example 1: Simple Commit

**You say:**
```
Run the commit.md workflow
```

**Cline interaction:**
```
📂 Current Status:

Modified files:
  src/components/Button.tsx
  src/components/Button.test.tsx

Changes:
  Button.tsx: Added 'variant' prop for primary/secondary styles
  Button.test.tsx: Added tests for variant prop

Nothing staged yet.

---

Should I stage all modified files? (yes/no)
```

**You:** `yes`

```
✅ Staged:
  src/components/Button.tsx
  src/components/Button.test.tsx

🔍 Running pre-commit hooks...
✅ ESLint: passed
✅ Prettier: passed
✅ Tests: passed

---

🎯 Proposed Commit Message:

feat(ui): add variant prop to Button component

Add primary and secondary variants to Button component for
consistent styling across the application.

- Added variant prop (primary | secondary)
- Updated styles for both variants
- Added comprehensive tests

Alternative 1:
feat(components): add Button variants

Alternative 2:
feat(ui): implement primary and secondary button styles

---

Approve and commit? (yes/no/edit)
```

**You:** `yes`

```
✅ Committed: abc123f
✅ Pushed to origin/feature/button-variants

Done! 🎉
```

---

### Example 2: Commit with Fixes Needed

**You say:**
```
Run the commit.md workflow
```

**Cline interaction:**
```
📂 Current Status:

Modified files:
  src/services/AuthService.ts
  src/services/AuthService.test.ts

Staging changes...

🔍 Running pre-commit hooks...

❌ ESLint: 3 errors

  src/services/AuthService.ts
    23:5   error  'user' is defined but never used  no-unused-vars
    45:12  error  Missing return type annotation    @typescript-eslint/explicit-function-return-type
    67:3   error  Expected '===' but saw '=='        eqeqeq

---

I can fix these automatically. Proceed? (yes/no)
```

**You:** `yes`

```
🔧 Applying fixes...

✅ Fixed:
- Removed unused 'user' variable
- Added return type annotation to validateToken()
- Changed '==' to '==='

🔍 Re-running hooks...
✅ All hooks passed!

---

🎯 Proposed Commit Message:

fix(auth): correct linting errors in AuthService

- Remove unused variable
- Add missing return type annotation
- Use strict equality operator

Approve and commit? (yes/no)
```

---

## Close Workflow Examples

### Example 1: Successful Feature

**You say:**
```
Run the close.md workflow
```

**Cline produces:**
```
📋 Feature Retrospective for MR !145

Story: US-4567 - Export user data to CSV
Merged: 2026-01-13 at 14:32
Duration: 3.2 days (estimate: 3 days)

---

## Acceptance Criteria Review

✅ AC1: Export users to CSV format
   Evidence: ExportService.ts, commit abc123f
   Tests: ExportService.test.ts (15 tests)

✅ AC2: Support pagination for large datasets  
   Evidence: Pagination implemented with streaming
   Tests: Integration tests with 5000 records

✅ AC3: Include rate limiting
   Evidence: rate-limiting.middleware.ts
   Tests: rate-limiting.spec.ts

✅ AC4: Secure against path traversal
   Evidence: Input sanitization in export.controller.ts
   Tests: security.test.ts

Verdict: ALL CRITERIA MET ✅

---

## Plan vs Reality

Planned tasks completed: 6/6 (100%)

Unplanned work:
- Added streaming support (not in original plan)
- Extra security review and fixes
- Performance optimization for large datasets

Why: Reviewer feedback led to improvements beyond original scope

---

## Quality Review

Tests: ✅ 45 new tests, all passing
Coverage: ✅ 89.2% (target: 75%)
SonarQube: ✅ Quality gate PASSED
Reviewer feedback: 3 threads, all resolved positively

Notable: Sarah suggested streaming which improved the solution significantly

---

## Estimate vs Actual

Baseline estimate: 3.0 man-days
Actual elapsed: 3.2 days (calendar)
Variance: +0.2 days (+7%)

Reason: Additional security work and streaming feature

---

## What Went Well

✅ Early detection of memory leak
✅ Proactive security review
✅ Good reviewer engagement
✅ Streaming suggestion improved the solution
✅ Tests comprehensive and maintainable

---

## What Could Improve

⚠️ Initial implementation missed edge cases
   → Action: Add more edge case thinking upfront

⚠️ Security review should have been earlier
   → Action: Add security checklist to planning phase

⚠️ Complexity spotted by SonarQube late
   → Action: Run SonarQube locally before pushing

---

## Improvements for Next Feature

Process:
1. Include security review in planning
2. Set up local SonarQube scanning

Technical:
1. Consider edge cases during design
2. Think about scale from the beginning

Estimation:
1. Add 10% buffer for security review
2. Current estimation accuracy: good

---

✅ Retrospective saved to: memory-bank/retro.md

🎉 Great job on this feature!
```

---

### Example 2: Feature with Challenges

**You say:**
```
Run the close.md workflow
```

**Cline produces:**
```
📋 Feature Retrospective for MR !167

Story: US-5012 - Real-time notifications
Merged: 2026-01-15 at 16:45
Duration: 7.5 days (estimate: 4 days)

---

## Acceptance Criteria Review

✅ AC1: Users receive notifications in real-time
   Evidence: WebSocket implementation
   
⚠️ AC2: Notifications persist when user offline
   Evidence: Partial - basic persistence only
   Note: Full offline sync deferred to US-5013

✅ AC3: Users can mark notifications as read
   Evidence: NotificationService.markAsRead()

✅ AC4: Unread count badge displayed
   Evidence: NotificationBadge component

Verdict: 3.5/4 CRITERIA MET (1 partial)

---

## Plan vs Reality

Planned tasks completed: 5/8 (62.5%)

Planned tasks skipped:
- Advanced offline sync (moved to next story)
- Push notifications (out of scope)
- Email fallback (deferred)

Unplanned work:
- WebSocket reconnection logic (not anticipated)
- Redis pub/sub for multi-server setup
- Extensive browser compatibility testing
- Performance optimization for 1000+ notifications

Why: Underestimated complexity of WebSocket reliability

---

## Quality Review

Tests: ✅ 67 tests (but integration tests weak)
Coverage: ⚠️ 78.1% (below goal of 85%)
SonarQube: ✅ Quality gate PASSED (after 3 attempts)
Reviewer feedback: 8 threads, 2 required major rework

Notable: WebSocket implementation needed two refactors

---

## Estimate vs Actual

Baseline estimate: 4.0 man-days
Actual elapsed: 7.5 days (calendar)
Variance: +3.5 days (+88%) ⚠️

Reason: 
- Underestimated WebSocket complexity (2 days)
- Multiple refactors needed (1.5 days)
- Browser compatibility issues (1 day)

---

## What Went Well

✅ Good communication with reviewers
✅ Incremental approach helped isolate issues
✅ Redis solution scaled well in testing
✅ Team provided good support

---

## What Could Improve

❌ Estimate was significantly off
❌ Testing strategy was insufficient initially
❌ Didn't research WebSocket reliability upfront
❌ Scope creep (multi-server wasn't in requirements)

---

## Improvements for Next Feature

Process:
1. Add "technical spike" phase for unfamiliar tech
2. Review estimates with senior dev for new tech
3. Stricter scope management

Technical:
1. Research reliability patterns before implementing
2. Plan integration tests during design phase
3. Test browser compatibility earlier

Estimation:
1. Add 2x buffer for new technologies
2. Break down complex features more granularly
3. Include time for research/learning

---

## Lessons Learned

🎓 WebSocket development has hidden complexity
🎓 Always plan for reconnection and error cases
🎓 Multi-server concerns should be discussed during planning
🎓 Integration tests are critical for real-time features

---

✅ Retrospective saved to: memory-bank/retro.md

💡 Despite challenges, the feature works well and the team learned a lot!
```

---

## 🎯 Key Takeaways

1. **Workflows automate the boring stuff** - Status updates, MR templates, commit messages
2. **Cline provides context** - Threads, SonarQube, pipelines in one place
3. **You stay in control** - Review everything before approving
4. **Retrospectives drive improvement** - Learn from each feature

---

**Want more examples? Just ask Cline:**
```
Show me an example of how to use the morning workflow
Can you walk me through a typical commit workflow?
What does a good retrospective look like?
```

