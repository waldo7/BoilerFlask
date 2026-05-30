---
status: testing
phase: 02-auth-system
source: 02-01-SUMMARY.md, 02-02-SUMMARY.md, 02-03-SUMMARY.md, 02-04-SUMMARY.md, 02-05-SUMMARY.md
started: 2026-05-30T15:09:00+08:00
updated: 2026-05-30T07:19:27Z
---

## Current Test

number: 2
name: Registration Flow (AUTH-01)
expected: |
  Visiting `/auth/register` renders a registration form with Email, Password, and Confirm Password fields. Submitting a new email and strong password redirects to the dashboard with a welcome message and creates the user in the database with role=user.
awaiting: user response

## Tests

### 1. Cold Start Smoke Test
expected: |
  Kill any running server/service. Clear ephemeral state (temp DBs, caches, lock files). Start the application from scratch. Server boots without errors, any seed/migration completes, and a primary query (health check, homepage load, or basic API call) returns live data.
result: pass

### 2. Registration Flow (AUTH-01)
expected: |
  Visiting `/auth/register` renders a registration form with Email, Password, and Confirm Password fields. Submitting a new email and strong password redirects to the dashboard with a welcome message and creates the user in the database with role=user.
result: pending

### 3. Login and Session Persistency (AUTH-02)
expected: |
  Visiting `/auth/login` renders a login form with Email, Password, and Remember Me fields. Logging in with valid credentials creates a session and redirects to the dashboard. Deactivated users cannot log in. Selecting Remember Me sets a persistent 30-day session cookie.
result: pending

### 4. Logout Flow (AUTH-03)
expected: |
  Visiting `/auth/logout` clears the user session and redirects to the home page `/`. Trying to access `/dashboard` after logging out redirects to `/auth/login`.
result: pending

### 5. Password Reset and itsdangerous Tokens (AUTH-04)
expected: |
  Visiting `/auth/forgot-password` and submitting an email (existing or unknown) shows a generic check email page to prevent user enumeration. The console (in dev mode) prints a password reset URL. Clicking the reset URL opens the Set New Password form. Submitting a new password updates the password, invalidates the token so it cannot be reused, and redirects to login.
result: pending

### 6. CLI Admin Commands (AUTH-05)
expected: |
  Running `flask create-admin` interactively prompts for email and password, validates password strength, and creates a user with role=admin. Running `flask set-admin <email> <role>` promotes or demotes a user's role.
result: pending

### 7. Password Show/Hide Toggle (D-22 / Manual)
expected: |
  On the login or register page, clicking the eye icon inside the password field toggles the password field visibility from masked (dots) to plain text.
result: pending

### 8. Mobile Responsiveness (MOB-02 / Manual)
expected: |
  Resizing the browser window to mobile viewports (e.g., 375px) shows the login and registration forms rendering in a clean, full-width, touch-friendly card layout.
result: pending

### 9. Rate Limiting Flash Message (D-31 / Manual)
expected: |
  Submitting a login or registration form rapidly 11+ times in a minute triggers rate limiting, returning a 429 status code and rendering a flash message "Too many attempts. Please try again later."
result: pending

### 10. Test Suite Passes (Automated)
expected: |
  Running `pytest` passes all 30 tests in the suite (4 skeleton tests + 26 auth tests) with zero failures.
result: pending

## Summary

total: 10
passed: 1
issues: 0
pending: 9
skipped: 0

## Gaps

- truth: "Server boots without errors on cold start; homepage returns live data"
  status: resolved
  reason: "Cold start failed: sqlite3.OperationalError: unable to open database file. Flask-SQLAlchemy 3.x resolved sqlite:///instance/app.db relative to instance_path, producing doubled instance/instance/app.db path."
  severity: blocker
  test: 1
  root_cause: "config.py line 10: SQLALCHEMY_DATABASE_URI used 'sqlite:///instance/app.db' — Flask-SQLAlchemy 3.x prepends instance_path to relative DB names, causing path doubling"
  artifacts:
    - path: "config.py"
      issue: "DB URI path doubled under Flask-SQLAlchemy 3.x"
  missing:
    - "Change SQLALCHEMY_DATABASE_URI default from 'sqlite:///instance/app.db' to 'sqlite:///app.db'"
  debug_session: ""
  resolved: true
