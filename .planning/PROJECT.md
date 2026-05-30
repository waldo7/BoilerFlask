# FlaskStuct

## What This Is

A modular Flask web application scaffold that provides authentication (registration, login, password reset), role-based access (admin/user), and a mobile-first sidebar layout — designed to be forked and expanded with additional features via blueprints without reinventing auth or layout.

## Core Value

Developers get a production-ready, organized Flask foundation with auth and responsive UI out of the box — so they can start building features immediately.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] AUTH-01: User can register with email and password
- [ ] AUTH-02: User can log in and session persists across browser refresh
- [ ] AUTH-03: User can log out from any page
- [ ] AUTH-04: User can request password reset via email
- [ ] AUTH-05: User has a role (admin or user) assigned at registration
- [ ] AUTH-06: Admin users see admin-only items in sidebar
- [ ] MAIN-01: Homepage shows "Flask app is running" placeholder
- [ ] MAIN-02: Authenticated users see dashboard after login
- [ ] MAIN-03: Sidebar renders Dashboard and Settings links
- [ ] LAYOUT-01: base.html provides consistent layout with Bootstrap 5
- [ ] LAYOUT-02: Error pages exist and are styled (403, 404, 500)
- [ ] MOB-01: Sidebar collapses to hamburger menu on screens < 768px
- [ ] MOB-02: All pages are readable and functional on 320px+ viewports
- [ ] MOB-03: Login/register forms are full-width and touch-friendly
- [ ] MOB-04: Dashboard layout stacks vertically on mobile

### Out of Scope

- REST API — Scaffold is server-rendered; API is separate concern
- OAuth / Social login — Third-party complexity; defer to v2
- Email verification — Requires real email infrastructure
- User profile editing — Not core scaffold; add later as feature
- Admin user management panel — Not core scaffold; add later as feature
- File uploads (avatars) — Storage complexity; defer to v2
- JS framework (React, Vue, HTMX) — User chose pure server-rendered

## Context

- **Who:** Individual developers or small teams who need a Flask starting point
- **Use case:** Fork → configure → add feature blueprints → deploy
- **Primary access:** Mobile devices (responsive-first design)
- **Environment:** Prototype on SQLite, migrate to PostgreSQL/MySQL in production
- **No existing code:** Greenfield project

## Constraints

- **Tech stack:** Flask 3.1+, Jinja, Bootstrap 5.3, SQLAlchemy, SQLite (dev) / PostgreSQL/MySQL (prod)
- **Architecture:** App factory pattern, blueprint-based, Jinja template inheritance
- **Frontend:** Server-rendered only — no JS framework, no build step
- **Mobile:** Must work at 320px+ viewports with touch-friendly controls

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| App factory over single app.py | Testable, multi-config, clean extension init | — Pending |
| Blueprint per domain (main/auth) | Loose coupling for future feature additions | — Pending |
| Werkzeug for password hashing (not bcrypt) | Ships with Flask, zero extra deps | — Pending |
| Bootstrap offcanvas for mobile sidebar | Native component, no JS framework needed | — Pending |
| SQLite for prototype, Postgres/MySQL for prod | Zero-config start, config-only migration path | — Pending |
| No Flask-Security — build auth manually | Keeps internals visible and extensible | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-30 after initialization*
