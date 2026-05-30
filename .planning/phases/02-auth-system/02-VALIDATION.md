---
phase: 2
slug: auth-system
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-30
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (already configured in Phase 1) |
| **Config file** | `tests/conftest.py` — `app` and `client` fixtures use `TestingConfig` |
| **Quick run command** | `pytest tests/test_auth.py -x` |
| **Full suite command** | `pytest tests/ -x` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_auth.py -x`
- **After every plan wave:** Run `pytest tests/ -x`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | AUTH-01 | T-02-01 | Registration form renders at GET /auth/register | unit | `pytest tests/test_auth.py::test_register_page -x` | ❌ W0 | ⬜ pending |
| 02-01-02 | 01 | 1 | AUTH-01 | T-02-04 | POST /auth/register creates user with hashed password | integration | `pytest tests/test_auth.py::test_register_success -x` | ❌ W0 | ⬜ pending |
| 02-01-03 | 01 | 1 | AUTH-01 | T-02-08 | Duplicate email rejected with WTForms error | integration | `pytest tests/test_auth.py::test_register_duplicate_email -x` | ❌ W0 | ⬜ pending |
| 02-01-04 | 01 | 1 | AUTH-01, AUTH-05 | T-02-04 | New user defaults to role=user server-side | unit | `pytest tests/test_auth.py::test_default_role -x` | ❌ W0 | ⬜ pending |
| 02-02-01 | 02 | 1 | AUTH-02 | T-02-05 | Login form renders at GET /auth/login | unit | `pytest tests/test_auth.py::test_login_page -x` | ❌ W0 | ⬜ pending |
| 02-02-02 | 02 | 1 | AUTH-02 | T-02-05 | Valid credentials create session | integration | `pytest tests/test_auth.py::test_login_success -x` | ❌ W0 | ⬜ pending |
| 02-02-03 | 02 | 1 | AUTH-02 | T-02-05 | Bad credentials show form error | integration | `pytest tests/test_auth.py::test_login_bad_credentials -x` | ❌ W0 | ⬜ pending |
| 02-02-04 | 02 | 1 | AUTH-02 | T-02-02 | Deactivated account rejected | integration | `pytest tests/test_auth.py::test_login_inactive_user -x` | ❌ W0 | ⬜ pending |
| 02-02-05 | 02 | 1 | AUTH-02 | T-02-07 | Remember me sets long-lived cookie | integration | `pytest tests/test_auth.py::test_login_remember_me -x` | ❌ W0 | ⬜ pending |
| 02-03-01 | 03 | 2 | AUTH-03 | T-02-09 | Logout clears session, redirects to / | integration | `pytest tests/test_auth.py::test_logout -x` | ❌ W0 | ⬜ pending |
| 02-04-01 | 04 | 2 | AUTH-04 | T-02-03 | Forgot-password form renders | unit | `pytest tests/test_auth.py::test_forgot_password_page -x` | ❌ W0 | ⬜ pending |
| 02-04-02 | 04 | 2 | AUTH-04 | T-02-03 | Existing email shows generic confirmation | integration | `pytest tests/test_auth.py::test_forgot_password_existing_email -x` | ❌ W0 | ⬜ pending |
| 02-04-03 | 04 | 2 | AUTH-04 | T-02-03 | Unknown email shows same confirmation (enumeration prevention) | integration | `pytest tests/test_auth.py::test_forgot_password_unknown_email -x` | ❌ W0 | ⬜ pending |
| 02-04-04 | 04 | 2 | AUTH-04 | T-02-06 | Valid reset token renders reset form | integration | `pytest tests/test_auth.py::test_reset_password_valid_token -x` | ❌ W0 | ⬜ pending |
| 02-04-05 | 04 | 2 | AUTH-04 | T-02-06 | Expired token shows error | integration | `pytest tests/test_auth.py::test_reset_password_expired_token -x` | ❌ W0 | ⬜ pending |
| 02-04-06 | 04 | 2 | AUTH-04 | T-02-06 | Reset success redirects to login with flash | integration | `pytest tests/test_auth.py::test_reset_password_success -x` | ❌ W0 | ⬜ pending |
| 02-05-01 | 05 | 2 | AUTH-05 | T-02-04 | CLI create-admin creates user with role=admin | integration | `pytest tests/test_auth.py::test_cli_create_admin -x` | ❌ W0 | ⬜ pending |
| 02-05-08 | 05 | 5 | AUTH-02 | T-02-01 | Unauthenticated user redirected to login | integration | `pytest tests/test_auth.py::test_dashboard_redirects_unauthenticated -x` | ❌ W0 | ⬜ pending |
| 02-05-09 | 05 | 5 | AUTH-02 | T-02-01 | Expired session redirects with flash message | integration | `pytest tests/test_auth.py::test_expired_session_redirect -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_auth.py` — stubs for AUTH-01 through AUTH-05 acceptance tests
- [ ] `tests/conftest.py` — update with `_db` fixture (SQLite in-memory) and `auth_client` fixture (FlaskLoginClient or manual session setup)
- [ ] Framework install: `pip install pytest` — verify present in venv from Phase 1

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Password show/hide toggle | D-22 | Browser JS interaction, not testable via pytest | Click eye icon, verify password field reveals text |
| Mobile auth form responsiveness | MOB-02 | Visual layout verification at specific viewports | Resize browser to 320px, 375px, 768px; verify forms are full-width and touch-friendly |
| Rate limit flash message rendering | D-31 | Time-dependent (10 req/min), impractical in unit tests | Submit login form rapidly 11+ times, verify flash "Too many attempts" |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
