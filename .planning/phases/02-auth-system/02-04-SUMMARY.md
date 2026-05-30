---
phase: 02-auth-system
plan: 04
subsystem: auth
tags: [flask-login, itsdangerous, flask-mail, flask-limiter, click, wtforms]

requires:
  - phase: 02-auth-system
    provides: "Wiring (create_app with extensions), UI (4 forms + 6 templates)"
provides:
  - "8 auth route handlers: login (GET/POST), register (GET/POST), logout, forgot-password (GET/POST), reset-password (GET/POST)"
  - "itsdangerous token-based password reset with 1-hour expiry and one-time use tracking"
  - "is_safe_url open redirect prevention"
  - "Rate limiting on all 4 POST endpoints (10/min) with flash-on-breach 429 handler"
  - "Dashboard stub with @login_required and empty state"
  - "Flask CLI: create-admin (interactive) and set-admin (role promotion)"
affects: [02-05-tests]

tech-stack:
  added:
    - "itsdangerous 2.2.0 (URLSafeTimedSerializer for reset tokens)"
  patterns:
    - "is_safe_url() uses urlparse netloc comparison for open redirect prevention"
    - "rate_limit() no-op wrapper for TestingConfig compatibility"
    - "register_commands(app) pattern for CLI command registration"
    - "password_reset_requested_at column for one-time token enforcement"

key-files:
  created:
    - "app/templates/dashboard.html - Protected dashboard with welcome message and empty state"
  modified:
    - "app/auth/routes.py - 8 route handlers + 5 helper functions (141 lines)"
    - "app/main/routes.py - Added @login_required /dashboard stub route"
    - "app/models/user.py - Added password_reset_requested_at column"
    - "app/__init__.py - Added 429 error handler and register_commands hook"
    - "app/commands.py - create-admin and set-admin CLI commands"

key-decisions:
  - "Password reset tokens use itsdangerous URLSafeTimedSerializer with salt='password-reset' and 1-hour max_age"
  - "One-time token enforcement via password_reset_requested_at column — set on token generation, cleared on successful reset"
  - "Forgot-password renders same page for found and not-found emails (D-06 user enumeration prevention)"
  - "Dev mode prints reset URL to console; prod dispatches via Flask-Mail with SMTP error catching"
  - "Rate limiting uses no-op decorator fallback when limiter is disabled (TestingConfig)"
  - "register_commands(app) pattern chosen over module-level app instance for test compatibility"

patterns-established:
  - "rate_limit() helper: returns limiter.limit('10 per minute') or no-op lambda"
  - "register_commands(app): Flask CLI commands as nested functions for clean testability"

requirements-completed: [AUTH-01, AUTH-02, AUTH-03, AUTH-04, AUTH-05]

duration: 7min
completed: 2026-05-30
---

# Phase 02 Plan 04: Logic Summary

**8 auth route handlers, itsdangerous password reset with one-time token enforcement, rate limiting, dashboard stub, and Flask CLI admin commands**

## Performance

- **Duration:** 7 min
- **Tasks:** 4 (merged into 2 commits for efficiency)
- **Files modified:** 5

## Accomplishments

- Created all 8 auth route handlers: login, register, logout, forgot-password, reset-password with GET/POST
- Implemented itsdangerous URLSafeTimedSerializer password reset with 1-hour expiry, one-time use via DB tracking (D-07)
- Added rate limiting (10/min) on 4 POST endpoints with flash-on-breach 429 handler (D-29/D-30/D-31)
- Created dashboard stub route protected by @login_required with empty state (D-16)
- Built Flask CLI commands: create-admin (interactive with password policy) and set-admin (role promotion)
- Added is_safe_url open redirect prevention (D-19)

## Task Commits

1. **Task 1+2+3: Core auth routes + password reset + dashboard** - `147d246`
2. **Task 4: CLI commands** - `fca5350`

## Files Created/Modified

- `app/auth/routes.py` - Complete: 8 route handlers, 5 helpers (141 lines)
- `app/main/routes.py` - Added /dashboard @login_required route
- `app/models/user.py` - Added password_reset_requested_at column for token tracking
- `app/__init__.py` - Added 429 error handler + register_commands hook
- `app/commands.py` - create-admin (interactive password prompt) + set-admin (role assignment)
- `app/templates/dashboard.html` - Protected dashboard with welcome + empty state

## Decisions Made

- Dashboard extends main base.html (not auth/base.html) — uses sidebar layout
- register_commands(app) pattern chosen to make CLI commands testable with test_cli_runner()
- Rate limiting POST endpoints only — GET endpoints are not rate-limited and return forms

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] CLI commands not testable with module-level app**

- **Found during:** Task 4 (CLI command verification)
- **Issue:** Original pattern created `app = create_app()` at module level, which registered commands on a singleton app. Test CLI runner uses `create_app('testing')` — a different instance — so commands weren't found.
- **Fix:** Refactored to `register_commands(app)` function called from `create_app()`, enabling test runner to access CLI commands.
- **Files modified:** app/commands.py, app/__init__.py, run.py
- **Verification:** `app.test_cli_runner().invoke(args=['create-admin'], ...)` succeeds
- **Committed in:** `fca5350`

**2. [Rule 2 - Missing Critical] Dashboard route needed before first register test (redirect dependency)**

- **Found during:** Task 1 (Core routes verification)
- **Issue:** Registration redirects to `url_for('main.dashboard')` but dashboard route didn't exist yet (scheduled for Task 3). Caused `BuildError` on redirect.
- **Fix:** Created dashboard route and template early (merged Task 3 into Task 1 commit) so register→dashboard redirect works.
- **Verification:** POST /auth/register → 302 → dashboard.html renders with Welcome message
- **Committed in:** `147d246`

---

**Total deviations:** 2 auto-fixed (1 rule 1, 1 rule 2)
**Impact on plan:** Both necessary for functional correctness. No scope creep.

## Issues Encountered

- Password reset routes already implemented in same file as core routes in one go — committed together
- Dashboard redirect dependency forced merged task execution order

## User Setup Required

None

## Next Phase Readiness

- Complete auth flow works: register → logout → login → password reset → dashboard
- Ready for Plan 02-05: Comprehensive test suite (conftest fixtures + test_auth.py)

---
*Phase: 02-auth-system*
*Completed: 2026-05-30*
