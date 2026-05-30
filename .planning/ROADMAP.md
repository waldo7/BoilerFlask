# Roadmap: FlaskStuct

**Created:** 2026-05-30
**Granularity:** Coarse (3 phases)
**Execution:** Sequential

---

### Phase 1: Project Skeleton
**Goal:** App factory, extensions, base template with Bootstrap 5, and placeholder homepage — the app starts and renders pages.

**Requirements:** MAIN-01, LAYOUT-01, LAYOUT-02, MOB-01, MOB-03

**Plans:** 4 plans

Plans:
- [x] 01-01-PLAN.md — Project config, requirements, .gitignore, config.py classes, pytest test scaffold
- [x] 01-02-PLAN.md — App factory (create_app), extensions.py placeholder, app.css custom styles
- [x] 01-03-PLAN.md — Jinja templates: base.html (Bootstrap+sidebar), home.html, error.html, about.html, contact.html
- [x] 01-04-PLAN.md — Blueprints (main + auth), route handlers, run.py entry point

**Success Criteria:**
1. [x] `python run.py` starts Flask without errors
2. [x] Visiting `/` displays homepage with "Flask app is running" placeholder
3. [x] `base.html` renders Bootstrap 5 layout with responsive navbar
4. [x] Sidebar collapses to hamburger on mobile viewports (< 768px)
5. [x] Error pages (404, 500) render with consistent styling
6. [x] Login/register forms render full-width and touch-friendly (structural responsiveness)

**UI hint:** yes

---

### Phase 2: Auth System
**Goal:** Complete authentication — registration, login, logout, password reset, and role-based user model.

**Requirements:** AUTH-01, AUTH-02, AUTH-03, AUTH-04, AUTH-05

**Plans:** 5/5 plans complete

Plans:
- [x] 02-01-PLAN.md — Foundation: packages, config keys, User model with Role enum
- [x] 02-02-PLAN.md — Wiring: create_app() extension wiring, auth_bp registration, auth CSS
- [x] 02-03-PLAN.md — UI: 4 WTForms classes + 6 Jinja auth templates
- [x] 02-04-PLAN.md — Logic: auth routes (8 handlers), dashboard stub, Flask CLI commands
- [x] 02-05-PLAN.md — Tests: test_auth.py (25+ tests), conftest fixtures

**Success Criteria:**
1. User can register with email and password via `/auth/register`
2. Registered user can login at `/auth/login` and session persists
3. User can logout from `/auth/logout`
4. User can request password reset via `/auth/forgot-password`
5. New users are assigned a role (admin/user)
6. Unauthenticated users are redirected to login when accessing protected pages

**UI hint:** yes

**Plans:** 5 plans

Plans:
- [x] 02-01-PLAN.md — Install auth packages, add config keys, create User model with Role enum
- [x] 02-02-PLAN.md — Wire extensions in create_app(), register auth_bp, add auth CSS, import routes
- [x] 02-03-PLAN.md — Create auth forms (4 WTForms classes) and auth templates (6 Jinja files)
- [x] 02-04-PLAN.md — Auth routes (8 handlers), dashboard stub, Flask CLI admin commands
- [ ] 02-05-PLAN.md — Comprehensive test suite (25+ tests, conftest DB/auth fixtures)

---

### Phase 3: Dashboard & Sidebar
**Goal:** Post-login dashboard with role-gated sidebar navigation, fully responsive on mobile.

**Requirements:** MAIN-02, MAIN-03, AUTH-06, MOB-02, MOB-04

**Success Criteria:**
1. Authenticated user sees dashboard at `/dashboard`
2. Sidebar shows Dashboard and Settings links
3. Admin users see additional admin-only sidebar items
4. Dashboard layout stacks vertically on mobile viewports
5. All pages are readable and functional at 320px width
6. Sidebar offcanvas opens/closes correctly on mobile touch

**UI hint:** yes
