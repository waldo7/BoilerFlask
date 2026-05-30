---
phase: 02-auth-system
plan: 01
subsystem: auth
tags: [sqlalchemy, flask-login, werkzeug, wtforms, flask-mail, flask-migrate, flask-limiter]

requires:
  - phase: 01-project-skeleton
    provides: "App factory, extensions.py stubs, config.py base, Jinja templates"
provides:
  - "9 auth packages installed with pinned versions"
  - "Auth, session, mail, and rate-limiting config keys across all environments"
  - "User model with Role enum (3 tiers), password hashing, and clean package import"
affects: [02-02-wiring, 02-03-ui, 02-04-logic, 02-05-tests]

tech-stack:
  added:
    - "Flask-SQLAlchemy 3.1.1"
    - "Flask-Login 0.6.3"
    - "Flask-WTF 1.3.0"
    - "Flask-Mail 0.10.0"
    - "Flask-Migrate 4.1.0"
    - "Flask-Limiter 4.1.1"
    - "email-validator 2.3.0"
    - "itsdangerous 2.2.0"
    - "Alembic 1.18.4"
    - "wtforms 3.2.2"
    - "Werkzeug 3.1.8 (explicitly pinned)"
  patterns:
    - "SQLAlchemy Enum for role storage"
    - "Werkzeug generate_password_hash / check_password_hash for password management"
    - "os.environ.get() with sensible defaults for all config keys"
    - "Explicit __init__ with kwargs.setdefault() for Python-level defaults"

key-files:
  created:
    - "app/models/__init__.py - Package-level User export"
    - "app/models/user.py - User model (7 columns), Role enum (3 values), password methods"
  modified:
    - "requirements.txt - Updated from 2 to 12 pinned packages"
    - ".env.example - Added 6 MAIL_* env var lines"
    - "config.py - Added 14 auth/session/mail/rate-limit config keys"

key-decisions:
  - "Pinned all 12 packages with exact versions for reproducible builds"
  - "MAIL_SUPPRESS_SEND=False in Config base class; route handlers check config to conditionally print console output in dev per D-05"
  - "RATELIMIT_DEFAULT set to 10/minute per D-30, disabled in testing to avoid 429 in integration tests"
  - "REMEMBER_COOKIE_DURATION=2592000 (30 days) per D-13"
  - "Role enum uses USER/ADMIN/SUPERUSER (lowercase values) per D-11"
  - "User.__init__ sets role and is_active defaults at Python level (SQLAlchemy defaults only apply at DB flush time)"

patterns-established:
  - "Package-level model import pattern: app/models/__init__.py re-exports User for clean 'from app.models import User'"

requirements-completed: [AUTH-05]

duration: 6min
completed: 2026-05-30
---

# Phase 02 Plan 01: Foundation Summary

**9 auth packages installed, 14 config keys added, User model with 3-tier Role enum and secure password hashing via Werkzeug**

## Performance

- **Duration:** 6 min
- **Started:** 2026-05-30T06:33:00Z
- **Completed:** 2026-05-30T06:39:00Z
- **Tasks:** 3
- **Files modified:** 5 (2 created, 3 modified)

## Accomplishments

- Installed 9 auth packages (SQLAlchemy, Login, WTF, Mail, Migrate, Limiter, email-validator, itsdangerous, Alembic) with pinned versions
- Added session security config (HttpOnly cookies, SameSite=Lax, 30-day remember-me), mail server config (6 env vars), and rate-limiting (10/min, memory:// storage)
- Created User model with 7 columns, Role enum (USER/ADMIN/SUPERUSER), and password hashing via Werkzeug

## Task Commits

Each task was committed atomically:

1. **Task 1: Install auth packages and update dependency files** - `a92b7f7` (feat)
2. **Task 2: Add auth and session config keys** - `92dc4ae` (feat)
3. **Task 3: Create User model with Role enum and password methods** - `8c82ff4` (feat)

## Files Created/Modified

- `requirements.txt` - 12 pinned packages (upgraded from 2)
- `.env.example` - 6 MAIL_* env var templates added
- `config.py` - 14 config keys across Config base + 3 subclasses
- `app/models/__init__.py` - Clean User re-export
- `app/models/user.py` - User model with 7 columns, Role enum, password methods

## Decisions Made

- Explicitly pinned Werkzeug==3.1.8 (ships with Flask 3.1.3 but should be locked for reproducibility)
- Used alembic==1.18.4 (lowercase in pip freeze — confirmed correct)
- User.__init__ uses kwargs.setdefault() for role and is_active defaults at Python object level (SQLAlchemy column defaults only apply at DB flush time)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] User model Python-level defaults missing**

- **Found during:** Task 3 (User model verification)
- **Issue:** SQLAlchemy's `default=` on Column only applies at INSERT/DB flush time, not when creating Python instances. `u.role == Role.USER` failed because role was None on a non-flushed instance.
- **Fix:** Added `__init__` to User model with `kwargs.setdefault('role', Role.USER)` and `kwargs.setdefault('is_active', True)` before calling `super().__init__(**kwargs)`.
- **Files modified:** app/models/user.py
- **Verification:** `python -c "from app.models import User; u = User(email='t@t.com'); assert u.role == Role.USER; assert u.is_active"` passes
- **Committed in:** `8c82ff4` (Task 3 commit)

---

**Total deviations:** 1 auto-fixed (rule 1)
**Impact on plan:** Required for Python-level model correctness. No scope creep.

## Issues Encountered

- pip freeze reports `alembic` (lowercase) while most other packages use TitleCase — grep needed `-i` flag
- SQLAlchemy column defaults are DB-level only; Python-level defaults require explicit init handling

## User Setup Required

None — no external service configuration required for this plan.

## Next Phase Readiness

- All 9 auth packages installed and importable
- Config keys defined for all environments (dev/prod/test)
- User model ready for wiring via create_app() (Plan 02-02)
- Ready for Plan 02-02: Extension wiring and blueprint registration

---
*Phase: 02-auth-system*
*Completed: 2026-05-30*
