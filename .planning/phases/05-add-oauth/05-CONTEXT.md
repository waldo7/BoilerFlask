# Phase 5: Add OAuth - Context

**Gathered:** 2026-05-30
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase introduces OAuth authentication (Google and GitHub) to the existing Flask application. It allows users to register and log in using third-party providers alongside the existing email/password system.

**Requirements:** AUTH-08
</domain>

<decisions>
## Implementation Decisions

### Account Linking
- **D-01:** If the OAuth email matches an existing account, auto-link them silently based on email (assuming Google and GitHub verify emails). This provides the smoothest UX following best practices.

### OAuth-only Users & Passwords
- **D-02:** Hide the "Change Password" form for OAuth-only users who haven't set a local password.
- **D-03:** Provide a "Set Password" option in the settings page for OAuth users who want to establish a local login fallback (following best practices).

### Provider Layout
- **D-04:** Place the Google and GitHub OAuth buttons directly on the main login and register forms (e.g., above or below the email/password fields) for high visibility.

### Missing Provider Emails
- **D-05:** If the OAuth provider doesn't return a public email, prompt the user to manually enter their email address to complete registration (following best practices).

### the agent's Discretion
- Exact styling and placement (above vs. below) of the OAuth buttons on the auth forms.
- The UI design of the "Set Password" form for OAuth-only users.
- Database schema changes (e.g., adding `github_id`, `google_id` columns to `User` model, or a separate `OAuth` model) to track provider links securely.
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project-Level Scope & Constraints
- `.planning/PROJECT.md` — Project definition, core value, active requirements, out of scope items, stack constraints. Key Decision: "OAuth via Flask-Dance when needed (v2) | Bolts onto existing Flask-Login session; no rewrite".
- `.planning/REQUIREMENTS.md` — List of all requirements; Phase 5 maps to AUTH-08.
- `.planning/ROADMAP.md` — Current phase success criteria.
- `.planning/STATE.md` — Active phase tracking and session progress.

### Prior Phase Context
- `.planning/phases/02-auth-system/02-CONTEXT.md` — Phase 2 context (User models, role enums, login/logout session states, redirect rules, email normalization).
- `.planning/phases/03-dashboard-sidebar/03-CONTEXT.md` — Phase 3 context (Dashboard routing, settings page with change password form).

### Extant Code & Layout Assets
- `app/templates/auth/base.html` — The standalone auth shell layout.
- `app/templates/auth/login.html` & `app/templates/auth/register.html` — The forms where OAuth buttons will be placed.
- `app/templates/settings.html` — Settings page where "Set Password" will be added.
- `app/models/user.py` — The user model file that will need updating to support OAuth linking.
- `app/auth/routes.py` — The auth blueprint where Flask-Dance routes will be registered.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `app/templates/auth/login.html` & `app/templates/auth/register.html` — Existing auth forms, ready for OAuth button injections.
- `app/models/user.py` — User model can be extended with OAuth provider IDs.
- `config.py` — Ready to store OAuth client IDs and secrets.

### Established Patterns
- **Blueprint routing**: Auth routes registered in `app/auth/routes.py` on `auth_bp`.
- **Session management**: Handled by Flask-Login in `app/extensions.py`. Flask-Dance integrates nicely with this.

### Integration Points
- `config.py` — Need to add `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, etc.
- `app/__init__.py` — Register Flask-Dance blueprints (e.g., `google_bp`, `github_bp`).
- `app/models/user.py` — Add OAuth tracking logic/columns.
- `app/auth/routes.py` — Add the callback logic to handle Flask-Dance responses and perform login/account linking.
</code_context>
