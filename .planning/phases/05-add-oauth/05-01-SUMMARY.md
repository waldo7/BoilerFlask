---
phase: 05-add-oauth
plan: 01
subsystem: auth
tags: [flask-dance, oauth2, google, github, sqlalchemy, flask-login]

# Dependency graph
requires:
  - phase: 02-auth-system
    provides: User model, login/logout, session management, password hashing
  - phase: 03-dashboard-sidebar
    provides: Settings page with change password form, sidebar layout
provides:
  - Google and GitHub OAuth login using Flask-Dance
  - OAuth model for provider linkage (SQLAlchemy + Flask-Login)
  - Nullable password_hash for OAuth-only users
  - "Set Password" form for users without local password
affects: [auth]

# Tech tracking
tech-stack:
  added: [Flask-Dance, blinker, requests-oauthlib]
  patterns: [init_oauth(app) factory pattern, oauth_authorized signal handler, SQLAlchemyStorage]

key-files:
  created:
    - app/auth/oauth.py
  modified:
    - requirements.txt
    - config.py
    - app/models/user.py
    - app/__init__.py
    - app/auth/forms.py
    - app/main/routes.py
    - app/templates/auth/login.html
    - app/templates/auth/register.html
    - app/templates/settings.html
    - tests/test_dashboard_settings.py

key-decisions:
  - "OAuth tokens stored in oauth table with user_id FK (not inline columns on User)"
  - "password_hash made nullable=True for clean OAuth-only user representation"
  - "init_oauth(app) factory function defers blueprint creation until config is available"
  - "OAuth buttons placed above form fields on login/register with SVG icons"
  - "GitHub email lookup iterates list for verified primary; Google uses /oauth2/v2/userinfo"

patterns-established:
  - "init_oauth(app) factory pattern: creates Google/GitHub blueprints inside create_app() so config is available"
  - "oauth_authorized signal handler: fetches email via provider API, links/creates user, logs in via Flask-Login"
  - "SQLAlchemyStorage backend: OAuth model inherits OAuthConsumerMixin, stores provider/token/user_id"

requirements-completed: [AUTH-08]

# Metrics
duration: 35m
completed: 2026-05-30
---

# Phase 5: Add OAuth Summary

**Flask-Dance OAuth with Google and GitHub providers, nullable passwords for OAuth-only users, and conditional Set Password settings form**

## Performance

- **Duration:** ~35 min
- **Started:** 2026-05-30T19:00:00Z
- **Completed:** 2026-05-30T19:35:00Z
- **Tasks:** 6
- **Files modified:** 11

## Accomplishments
- Flask-Dance[sqla] and blinker added to requirements
- OAuth client ID/secret config keys in config.py with env var support
- OAuth model with OAuthConsumerMixin and User FK; password_hash made nullable
- Google and GitHub blueprints created via init_oauth() factory, registered in app
- SVG-branded OAuth buttons on login and register forms
- Conditional settings form: "Set Password" for OAuth users, "Change Password" for email users

## Task Commits

Each task was committed atomically:

1. **Task 1: 01-dependencies** - `fbd4919` (feat)
2. **Task 2: 02-configuration** - `6da4ea0` (feat)
3. **Task 3: 03-database-models** - `91429f9` (feat)
4. **Task 4: 04-oauth-logic** - `4070947` (feat)
5. **Task 5: 05-templates-auth** - `f912a87` (feat)
6. **Task 6: 06-settings-password** - `b567e2e` (feat)

## Files Created/Modified
- `requirements.txt` - Added Flask-Dance[sqla] and blinker
- `config.py` - Added GOOGLE_OAUTH_CLIENT_ID/SECRET and GITHUB_OAUTH_CLIENT_ID/SECRET
- `.env.example` - Added OAuth env var placeholders
- `app/models/user.py` - OAuth model, password_hash nullable, check_password guard
- `app/models/__init__.py` - Export OAuth alongside User
- `migrations/` - Initial migration setup with oauth table and nullable password alteration
- `app/auth/oauth.py` - OAuth blueprints (Google + GitHub), signal handlers, SQLAlchemyStorage backend
- `app/__init__.py` - init_oauth() call in create_app
- `app/auth/forms.py` - SetPasswordForm (password + confirm, no current_password)
- `app/main/routes.py` - Conditional form selection in settings route
- `app/templates/auth/login.html` - Google/GitHub OAuth buttons above form
- `app/templates/auth/register.html` - Google/GitHub OAuth buttons above form
- `app/templates/settings.html` - Conditional "Set Password" vs "Change Password" rendering
- `tests/test_dashboard_settings.py` - test_settings_oauth_user_set_password

## Decisions Made
- Used `init_oauth(app)` factory pattern instead of module-level blueprint creation to ensure config is loaded before blueprint construction (app factory compatibility)
- Correct import path is `flask_dance.consumer.storage.sqla`, not `.backend.sqla` (upstream docs need updating)
- Set `_user_id` in session for testing OAuth user (can't log in via form since no password exists)

## Deviations from Plan

### Auto-fixed Issues

**1. Correct import path for OAuthConsumerMixin**
- **Found during:** Task 3 (Database models)
- **Issue:** Plan referenced `flask_dance.consumer.backend.sqla` which doesn't exist in Flask-Dance 7.1.0
- **Fix:** Changed to `flask_dance.consumer.storage.sqla` and used `SQLAlchemyStorage` instead of `SQLAlchemyBackend`
- **Files modified:** app/models/user.py, app/auth/oauth.py
- **Committed in:** 91429f9 (Task 3 commit)

**2. Blueprint lazy initialization**
- **Found during:** Task 4 (OAuth logic)
- **Issue:** Module-level blueprint creation with `current_app.config` fails in app factory pattern (config not available at import time)
- **Fix:** Created `init_oauth(app)` factory function called inside `create_app()` after config is loaded
- **Files modified:** app/auth/oauth.py, app/__init__.py
- **Committed in:** 4070947 (Task 4 commit)

---

**Total deviations:** 2 auto-fixed (1 import path correction, 1 initialization pattern)
**Impact on plan:** Both auto-fixes essential for correctness with Flask-Dance 7.1.0 and app factory compatibility. No scope creep.

## Issues Encountered
- Migrations directory didn't exist; had to `flask db init` before `flask db migrate`
- Dev DB already had users table; Alembic auto-detected oauth table addition and nullable alteration correctly

## User Setup Required

To use OAuth login, add the following to `.env`:
- `GOOGLE_OAUTH_CLIENT_ID` — from Google Cloud Console (APIs & Services > Credentials)
- `GOOGLE_OAUTH_CLIENT_SECRET` — from Google Cloud Console
- `GITHUB_OAUTH_CLIENT_ID` — from GitHub Developer Settings > OAuth Apps
- `GITHUB_OAUTH_CLIENT_SECRET` — from GitHub Developer Settings

Authorized redirect URIs must include:
- `http://localhost:5000/login/google/authorized`
- `http://localhost:5000/login/github/authorized`

## Next Phase Readiness
- OAuth integration complete with Google and GitHub
- New requirement: AUTH-08 (OAuth login) fulfilled
- All 36 tests pass (35 existing + 1 new OAuth settings test)

---
*Phase: 05-add-oauth*
*Completed: 2026-05-30*
