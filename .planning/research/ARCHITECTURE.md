# Architecture Research: Flask Scaffold

## Component Boundaries

```
┌─────────────────────────────────────────┐
│                 run.py                   │
│            (entry point)                 │
└────────────────┬────────────────────────┘
                 │ from app import create_app
┌────────────────▼────────────────────────┐
│            app/__init__.py               │
│          create_app(config)              │
│  ┌──────────┐  ┌──────────────────────┐ │
│  │ Register │  │ Register extensions  │ │
│  │blueprints│  │(db, login, wtf,mail) │ │
│  └──────────┘  └──────────────────────┘ │
└──────┬──────────────────────┬───────────┘
       │                      │
┌──────▼──────┐        ┌──────▼──────┐
│ main/       │        │ auth/       │
│ Blueprint   │        │ Blueprint   │
│ url: /      │        │ url: /auth  │
├─────────────┤        ├─────────────┤
│ routes.py   │        │ routes.py   │
│ utils.py    │        │ forms.py    │
│             │        │ utils.py    │
└──────┬──────┘        └──────┬──────┘
       │                      │
       └──────────┬───────────┘
                  │
┌─────────────────▼────────────────────────┐
│            models/user.py                 │
│         (shared across blueprints)        │
└─────────────────┬────────────────────────┘
                  │
┌─────────────────▼────────────────────────┐
│           extensions.py                   │
│   db = SQLAlchemy()                      │
│   login = LoginManager()                 │
│   csrf = CSRFProtect()                   │
│   mail = Mail()                          │
└───────────────────────────────────────────┘
```

## Data Flow

```
1. Request hits Flask → Blueprint route matched
2. Route handler (routes.py) → queries models → renders template
3. Forms submit → POST route → validate (forms.py) → model ops → redirect
4. Auth: login → Flask-Login sets session cookie → @login_required gates
5. Templates: Jinja2 renders with {% extends "base.html" %} → Bootstrap 5 CSS
```

## Build Order (dependencies)

```
Phase 1: Project Skeleton
  ├── config.py + extensions.py + app/__init__.py (factory)
  ├── base.html (layout + Bootstrap + mobile meta)
  └── home.html (placeholder homepage)

Phase 2: Auth System
  ├── models/user.py (depends on Phase 1 extensions)
  ├── auth/ blueprint (depends on user model)
  └── auth templates (depends on base.html)

Phase 3: Dashboard + Sidebar
  ├── dashboard route (depends on auth → @login_required)
  ├── sidebar template (depends on base.html)
  └── admin gating (depends on user.role)
```

## Key Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| App factory over single app.py | Testable, multi-config, clean extension init |
| Blueprint per domain | Loose coupling; add features = add blueprints |
| Shared models/ directory | Single source of truth for DB schema |
| Extensions in separate file | Avoid circular imports (common Flask footgun) |
| config.py with classes | Env-based switching: Dev/Prod/Test |
