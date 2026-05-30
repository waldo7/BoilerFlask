---
phase: 02-auth-system
plan: 02
subsystem: auth
tags: [flask-login, flask-migrate, flask-limiter, flask-mail, csrf, sqlalchemy]

requires:
  - phase: 02-auth-system
    provides: "Flask-SQLAlchemy db instance, User model with Role enum, pinned packages"
provides:
  - "Fully wired app factory with db, login_manager, csrf, mail, migrate, and rate limiter"
  - "user_loader callback with is_active deactivation gate (D-25)"
  - "auth_bp Blueprint registered at /auth prefix"
  - "Dev database bootstrap with inspect.has_table() guard"
  - "Auth form centering CSS with UI-SPEC compliant card layout"
affects: [02-03-ui, 02-04-logic, 02-05-tests]

tech-stack:
  added: []
  patterns:
    - "Extension wiring via init_app() pattern in create_app()"
    - "user_loader closure pattern inside create_app()"
    - "Limiter constructor pattern (not init_app)"
    - "Dev db.create_all() with sqlalchemy.inspect guard"

key-files:
  modified:
    - "app/__init__.py - create_app() now wires 6 extensions, registers auth_bp, user_loader, dev DB bootstrap"
    - "app/auth/__init__.py - Routes import appended after blueprint creation"
    - "app/auth/routes.py - Minimal stub (routes filled in Plan 02-04)"
    - "app/static/css/app.css - 11 auth-specific CSS rules for centered card forms"

key-decisions:
  - "Flask-Limiter created with constructor pattern (not init_app) per RESARCH.md Pattern 4"
  - "user_loader returns None for is_active=False to terminate deactivated user sessions per D-25"
  - "Dev DB bootstrap runs only when DEBUG=True and TESTING=False, uses inspect.has_table() to avoid recreating existing tables"
  - "login_manager.session_protection='basic' for session ID regeneration on login per D-15"

patterns-established:
  - "routes.py stub pattern: create placeholder file when blueprint needs routes import before actual routes exist"

requirements-completed: [AUTH-02]

duration: 4min
completed: 2026-05-30
---

# Phase 02 Plan 02: Wiring Summary

**App factory wired with 6 extensions, auth blueprint registered, user_loader with deactivation gate, dev DB bootstrap, and auth-specific CSS**

## Performance

- **Duration:** 4 min
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Wired db, login_manager, csrf, mail, migrate, and limiter into create_app()
- Added user_loader callback with is_active deactivation gate per D-25
- Registered auth_bp Blueprint at /auth prefix in create_app()
- Created auth routes.py stub to satisfy import in __init__.py
- Added 11 auth-specific CSS rules (centered card, form labels, submit button, cross-links, mobile responsive) per UI-SPEC

## Task Commits

1. **Task 1: Wire extensions in create_app()** - `227d515`
2. **Task 2: Import routes and auth CSS** - `d144093`

## Files Created/Modified

- `app/__init__.py` - 47 new lines: extension wiring, auth_bp registration, user_loader, dev DB bootstrap
- `app/auth/__init__.py` - Routes import appended
- `app/auth/routes.py` - Placeholder stub (to be filled in Plan 02-04)
- `app/static/css/app.css` - Auth-specific CSS block (11 rules)

## Decisions Made

- Limiter uses constructor pattern (Limiter(...)) rather than init_app per RESEARCH.md
- routes.py stub created to prevent circular import on auth_bp import (Plan 02-04 will fill it)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] routes.py stub not specified in plan**

- **Found during:** Task 2 (Routes import in auth/__init__.py)
- **Issue:** Plan says to add `from app.auth import routes` but routes.py doesn't exist until Plan 02-04. Python raises ImportError on auth_bp import.
- **Fix:** Created minimal routes.py stub file so the import succeeds. Plan 02-04 will replace this with full route handlers.
- **Files modified:** app/auth/routes.py (created)
- **Verification:** `python -c "from app.auth import auth_bp; print(auth_bp.url_prefix)"` prints /auth, app boots with 200 on /
- **Committed in:** `d144093`

---

**Total deviations:** 1 auto-fixed (rule 2)
**Impact on plan:** Required for app to boot. Stub is a no-op until Plan 02-04 fills it in. No scope creep.

## Issues Encountered

- Circular import error when adding routes import before routes.py exists — resolved with stub file

## User Setup Required

None

## Next Phase Readiness

- create_app() fully wires all extensions
- auth_bp registered and importable
- User model accessible via user_loader
- Ready for Plan 02-03: WTForms and Jinja auth templates

---
*Phase: 02-auth-system*
*Completed: 2026-05-30*
