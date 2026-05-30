# Phase 1: Project Skeleton - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-30
**Phase:** 01-project-skeleton
**Areas discussed:** Template structure & layout pattern, Sidebar navigation content, Error page design & messaging, Mobile responsiveness depth

---

## Template Structure & Layout

| Option | Description | Selected |
|--------|-------------|----------|
| Single base.html | One base.html with well-named blocks. Pages extend directly. Sufficient for this scaffold's scope. | ✓ |
| Two-level: base.html → layout.html | base.html has minimal shell; layout.html adds sidebar + nav. Cleaner separation but extra file. | |
| Three-level: base → layout → page | Max flexibility but adds complexity the scaffold doesn't need yet. | |

| Option | Description | Selected |
|--------|-------------|----------|
| In base.html | Sidebar rendered in base.html — every page gets it automatically. | ✓ |
| Included via {% include %} | Sidebar as separate _sidebar.html partial, included per-page. | |
| Block in base, pages opt in | Sidebar defined as empty block; pages fill if they want it. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Fixed on desktop, offcanvas on mobile | Sidebar visible at >=768px; hamburger offcanvas below. Standard Bootstrap pattern. | ✓ |
| Offcanvas-only at all sizes | Sidebar always hidden behind toggle. Clean but extra click on desktop. | |
| Fixed sidebar, collapse to top navbar | Sidebar becomes collapsed top navbar on mobile. Simpler JS, less screen real estate. | |

| Option | Description | Selected |
|--------|-------------|----------|
| CDN | Bootstrap CSS/JS from official CDN. Zero build step, fast edge delivery. | ✓ |
| Local static files | Download and serve from app/static/. Works offline but adds maintenance. | |

**Notes:** User consistently chose the simplest, most standard approach for templates — single inheritance, CDN, fixed+offcanvas pattern. No deferred ideas from this area.

---

## Sidebar Navigation Content

| Option | Description | Selected |
|--------|-------------|----------|
| Placeholder links | Dashboard and Settings links visible but point to placeholder/homepage. Establishes UI structure. | ✓ |
| Login + Register links | Show actionable links for what's available now without auth. | |
| Minimal — just brand/title | Sidebar contains only app name. Clean but empty. | |

| Option | Description | Selected |
|--------|-------------|----------|
| App name + Bootstrap icon | Display "FlaskStuct" + Bootstrap Icons CDN icon at sidebar top. | ✓ |
| App name text only | Plain text at sidebar top. No image dependency. | |
| No brand header | Skip brand area entirely. Simpler but less polished. | |

| Option | Description | Selected |
|--------|-------------|----------|
| No — basic links only | Just Dashboard and Settings. Admin gating deferred to Phase 3. | ✓ |
| Show admin links but ungated | Add Admin link visible to everyone. Structure exists; gating added later. | |
| Stub admin link with comment | Commented-out admin section in template. Developers can see the pattern. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Bootstrap .active class | Bootstrap's built-in .active class with highlighted background. | ✓ |
| Custom underline indicator | Colored left border on active link. Subtle, requires custom CSS. | |
| No active state for Phase 1 | Skip. Active states wired in Phase 3. | |

**Notes:** Placeholder links chosen to show the structure without wiring real pages yet. Admin gating explicitly deferred to Phase 3. Bootstrap Icons CDN for brand icon.

---

## Error Page Design & Messaging

| Option | Description | Selected |
|--------|-------------|----------|
| Standalone minimal pages | Own lightweight templates — no sidebar, no complex nav. Prevents broken sidebar from compounding errors. | ✓ |
| Extend base.html with sidebar | Full layout including sidebar. Consistent but sidebar may not be useful on error. | |
| Extend base but sidebar conditional | Error pages extend base.html but sidebar block is empty. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Friendly + helpful | "Oops! Page not found." with clear "Go Home" button. Human, not intimidating. | ✓ |
| Technical/Terse | Standard HTTP status name and code. Accurate but less welcoming. | |
| Dev-friendly with debug hint | "Check the URL or return home." Extra detail for development. | |

| Option | Description | Selected |
|--------|-------------|----------|
| App name + Bootstrap icon | App name and relevant Bootstrap icon per error code. | ✓ |
| Just the error message | Plain text error code + message + button. Absolutely minimal. | |
| Full brand header from base.html | Pull in same brand/logo treatment from normal pages. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Single template with variables | One error.html accepting code, title, message. DRY, easy to add new codes. | ✓ |
| Individual templates per code | Separate 403.html, 404.html, 500.html. Maximum flexibility. | |

**Notes:** Error pages deliberately kept independent of base.html to avoid cascading failures. Single error.html with variables chosen for DRYness. Bootstrap Icons reused for error page branding.

---

## Mobile Responsiveness Depth

| Option | Description | Selected |
|--------|-------------|----------|
| Structural only | Viewport meta, sidebar hamburger at 768px, base responsive grid. Per-page polish deferred to Phase 3. | ✓ |
| Structural + form pages | All mobile behavior now — responsive sidebar, touch-friendly forms, stacked layouts. | |
| Bare minimum | Just viewport meta + sidebar toggle. Everything else uses Bootstrap defaults. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Minimal custom CSS file | Small app/static/css/app.css with essential overrides — sidebar width, content padding, hamburger styling. | ✓ |
| Bootstrap-only, no custom CSS | Use Bootstrap utility classes exclusively. No custom stylesheet. | |
| Custom CSS with mobile-first media queries | Full custom stylesheet with explicit breakpoints. More polish but adds maintenance. | |

| Option | Description | Selected |
|--------|-------------|----------|
| Full bundle with Popper | bootstrap.bundle.min.js — includes Popper for offcanvas. Required for sidebar. | ✓ |
| Bootstrap JS only, no Popper | Lighter but offcanvas requires Popper — sidebar won't work. | |

| Option | Description | Selected |
|--------|-------------|----------|
| End of body | Scripts at bottom of <body> in base.html. Standard performance practice. | ✓ |
| Head with defer | Scripts in <head> with defer. Renders sooner. | |

**Notes:** Structural-only approach respects the phase boundary — Phase 3 owns MOB-02 and MOB-04 mobile polish. Bootstrap bundle with Popper is non-negotiable for offcanvas. Minimal custom CSS keeps the scaffold lean.

---

## the agent's Discretion

- Exact Bootstrap icon choice for sidebar brand and error pages
- Custom CSS specifics beyond structural decisions (pixel values, hover states)
- Jinja block naming beyond `head`, `content`, `sidebar`, `scripts`
- Exact error page messaging wording
- Whether to include favicon link in base.html

## Deferred Ideas

- Admin-only sidebar links with role gating → Phase 3 (AUTH-06)
- Full mobile polish (320px+, dashboard stacking) → Phase 3 (MOB-02, MOB-04)
- Login/Register form touch-friendly sizing → Phase 2
- Bootstrap Icons local fallback → deferred indefinitely
- Dark mode toggle → not in v1 scope
