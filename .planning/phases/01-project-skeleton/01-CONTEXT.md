# Phase 1: Project Skeleton - Context

**Gathered:** 2026-05-30
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase delivers the Flask application foundation: the app boots via `python run.py`, serves a homepage with "Flask app is running" placeholder, provides a consistent Bootstrap 5 layout through `base.html`, includes styled error pages (403, 404, 500), and implements a responsive sidebar that collapses to a hamburger menu on mobile viewports (< 768px). No authentication, no user model, no dashboard — that's Phase 2 and 3.

**Requirements:** MAIN-01, LAYOUT-01, LAYOUT-02, MOB-01, MOB-03
</domain>

<decisions>
## Implementation Decisions

### Template Structure & Layout
- **D-01:** Single `base.html` with well-named Jinja blocks (`head`, `content`, `sidebar`, `scripts`). All pages extend `base.html` directly — no intermediate layout templates.
- **D-02:** Sidebar is rendered in `base.html`. Every page gets it automatically via the base template.
- **D-03:** Fixed sidebar visible on desktop (>= 768px). On mobile (< 768px), sidebar hides behind a hamburger toggle and slides in via Bootstrap offcanvas component.
- **D-04:** Bootstrap 5.3 CSS and JS loaded from CDN — no local static Bootstrap files.

### Sidebar Navigation Content
- **D-05:** Sidebar shows placeholder links: Dashboard and Settings. These link to placeholder pages or homepage until wired in Phase 3.
- **D-06:** Sidebar brand header shows app name "FlaskStuct" + a Bootstrap icon (e.g., house/grid icon) from Bootstrap Icons CDN.
- **D-07:** No admin-only links in Phase 1. Role-gated sidebar items are deferred to Phase 3.
- **D-08:** Current page indicated with Bootstrap `.active` class on the sidebar link.

### Error Page Design
- **D-09:** Error pages (403, 404, 500) are standalone minimal templates — they do NOT extend `base.html`. Prevents broken sidebar/nav from compounding an error state.
- **D-10:** Error messaging uses friendly, helpful tone (e.g., "Oops! Page not found.") with a clear "Go Home" button.
- **D-11:** Error pages show app name + a relevant Bootstrap icon (exclamation-triangle for 500, question-circle for 404) as branding.
- **D-12:** Single `error.html` template shared across all error codes — accepts code, title, and message as variables. Register error handlers in `create_app()`.

### Mobile Responsiveness
- **D-13:** Structural mobile responsiveness only: viewport meta tag, sidebar hamburger collapse at 768px, and base template responsive grid. Individual page mobile polish (form widths, stacked layouts) deferred to Phase 3 per MOB-02 and MOB-04.
- **D-14:** A minimal custom CSS file at `app/static/css/app.css` with essential overrides: sidebar width, content padding when sidebar is visible, mobile hamburger styling. No framework — just targeted overrides.
- **D-15:** Bootstrap JS bundle with Popper (`bootstrap.bundle.min.js`) from CDN — required for offcanvas sidebar component.
- **D-16:** All scripts placed at end of `<body>` in `base.html` (standard performance practice).

### the agent's Discretion
- Exact Bootstrap icon choice for sidebar brand and error pages (researcher/planner picks from Bootstrap Icons CDN)
- Custom CSS specifics beyond the decisions above (specific pixel values, hover states)
- Jinja block naming beyond the core blocks: `head`, `content`, `sidebar`, `scripts`
- Exact wording of error page messages beyond the friendly/helpful tone
- Whether to include a favicon link in base.html
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project-Level
- `.planning/PROJECT.md` — Project scope, constraints, key decisions (app factory, blueprints, Bootstrap offcanvas, SQLite, no Flask-Security)
- `.planning/REQUIREMENTS.md` — Full v1 requirements; Phase 1 covers MAIN-01, LAYOUT-01, LAYOUT-02, MOB-01, MOB-03
- `.planning/ROADMAP.md` — Phase 1 goal and success criteria (6 items)
- `.planning/STATE.md` — Project state tracking

### Architecture Research
- `.planning/research/ARCHITECTURE.md` — Component boundaries (app factory, extensions, blueprints), data flow, build order
- `.planning/research/STACK.md` — Recommended stack: Flask 3.1+, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Bootstrap 5.3, Werkzeug, python-dotenv

### Pitfalls (Phase 1 relevant)
- `.planning/research/PITFALLS.md` §1 — Circular imports: use `extensions.py` pattern from day one
- `.planning/research/PITFALLS.md` §5 — Mobile nav not working: Bootstrap offcanvas, JS bundle, viewport meta tag
- `.planning/research/PITFALLS.md` §6 — Hardcoded config: config classes, env vars for secrets
- `.planning/research/PITFALLS.md` §7 — Missing error handlers: register in `create_app()`, styled error pages
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None — greenfield project, no existing code

### Established Patterns
- App factory pattern (`create_app()` in `app/__init__.py`) — from PROJECT.md and ARCHITECTURE.md
- Extensions pattern (`extensions.py` with `init_app()` calls) — prevents circular imports
- Blueprint-per-domain: `main/` (prefix `/`) and `auth/` (prefix `/auth`)
- Config class hierarchy: `Config` base → `DevelopmentConfig` / `ProductionConfig`

### Integration Points
- `run.py` → `create_app()` (entry point)
- `app/__init__.py` → register blueprints, extensions, error handlers
- `config.py` → configuration classes, env var loading
- `extensions.py` → extension instances (db, login, csrf, mail)
</code_context>

<specifics>
## Specific Ideas

- Homepage should display "Flask app is running" as a visible confirmation the scaffold works (MAIN-01)
- Bootstrap Icons CDN for sidebar brand icon and error page icons — lightweight, zero extra deps
- Error handlers registered in `create_app()` using `@app.errorhandler(code)` decorator pattern
- Sidebar uses Bootstrap offcanvas component with `offcanvas-start` class for mobile slide-in behavior
</specifics>

<deferred>
## Deferred Ideas

- Admin-only sidebar links with role gating → Phase 3 (AUTH-06)
- Full mobile polish (320px+ readability, dashboard vertical stacking) → Phase 3 (MOB-02, MOB-04)
- Login/Register form touch-friendly sizing → Phase 2 (MOB-03 full implementation — structural responsiveness from Phase 1 is sufficient)
- Bootstrap Icons local fallback (only CDN for now)
- Dark mode toggle (not in scope for v1)
</deferred>

---

*Phase: 01-project-skeleton*
*Context gathered: 2026-05-30*
