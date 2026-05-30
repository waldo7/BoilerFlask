# Research Summary: Flask Scaffold

## Key Findings

### Stack
- Flask 3.1+ with Flask-SQLAlchemy (3.1+), Flask-Login (0.6+), Flask-WTF (1.2+)
- Werkzeug for password hashing (ships with Flask), itsdangerous for reset tokens
- Bootstrap 5.3 for mobile-first UI — offcanvas component for sidebar
- SQLite → PostgreSQL/MySQL via connection string swap only
- **Avoid:** Flask-Security (over-engineered), Django (wrong framework), HTMX (JS dependency)

### Table Stakes
12 core features across 3 categories: Auth (6), Layout (2), Main (4)
- All auth flows are standard and well-documented in Flask ecosystem
- Mobile responsiveness is critical — Bootstrap 5 handles this natively
- Dependencies: Dashboard needs auth, admin gating needs roles, sidebar needs layout

### Watch Out For
1. **Circular imports** — use `extensions.py` pattern from day one
2. **Password hashing** — never store plaintext; use Werkzeug built-in
3. **CSRF** — always include `{{ form.hidden_tag() }}` in forms
4. **Mobile sidebar** — use Bootstrap offcanvas, not just CSS hide/show
5. **Hardcoded config** — env vars for secrets, config classes for envs
6. **Error handlers** — register 403/404/500 in factory; styled error pages

### Architecture
- App factory pattern with `create_app(config)`
- Blueprint-per-domain: `main/` (/) and `auth/` (/auth)
- Shared `models/` directory, `extensions.py` for init-once pattern
- Build order: Skeleton → Auth → Dashboard (strict dependency chain)
