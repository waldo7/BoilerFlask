# Phase 1: Project Skeleton - Research

**Researched:** 2026-05-30
**Domain:** Flask web application scaffold — app factory, Bootstrap 5.3 layout, responsive sidebar
**Confidence:** HIGH

## Summary

Phase 1 establishes the FlaskStuct foundation: an app-factory-based Flask 3.1.3 application that boots via `python run.py`, serves a placeholder homepage, provides a Bootstrap 5.3.8 base layout with a responsive sidebar (fixed on desktop >= 768px, offcanvas hamburger on mobile), and renders styled error pages (403, 404, 500) from a single shared template.

This is a pure scaffold phase — no authentication, no database models, no forms. Every file is created from scratch on a greenfield project. The architecture follows the established pattern from ARCHITECTURE.md: `run.py` → `create_app()` → register blueprints, extensions, and error handlers. The Bootstrap responsive offcanvas component (`offcanvas-md`) provides the sidebar collapse behavior with zero JavaScript custom code — it relies entirely on Bootstrap's data-attribute-driven JS.

**Primary recommendation:** Create all files in dependency order (config first, then extensions, then factory, then blueprints, then templates). Use Bootstrap 5.3.8 CDN with integrity hashes for CSS, JS bundle (with Popper), and Bootstrap Icons web font. Register error handlers via `app.register_error_handler()` in `create_app()` using a shared `error.html` template.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| App boot / entry | API/Backend (run.py) | — | Single entry point, no frontend involvement |
| Configuration loading | API/Backend (config.py) | — | Server-side config, env var resolution |
| Blueprint registration | API/Backend (create_app) | — | Route registration happens server-side |
| Template rendering | Frontend Server (Jinja) | — | Server-rendered, no client-side routing |
| Sidebar layout | Frontend Server (Jinja) + Browser (Bootstrap CSS) | — | base.html renders structure, Bootstrap CSS positions it |
| Sidebar toggle (mobile) | Browser (Bootstrap JS) | — | Offcanvas component is client-side JS only |
| Error page rendering | Frontend Server (Jinja) | — | Error handlers call render_template server-side |
| Static CSS | CDN/Static (Browser) | — | Served from CDN (Bootstrap) and Flask static route (app.css) |
| Viewport meta / responsive breakpoints | Browser | — | Meta tag in head, Bootstrap CSS media queries |

## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Single `base.html` with well-named Jinja blocks (`head`, `content`, `sidebar`, `scripts`). All pages extend `base.html` directly — no intermediate layout templates.
- **D-02:** Sidebar is rendered in `base.html`. Every page gets it automatically via the base template.
- **D-03:** Fixed sidebar visible on desktop (>= 768px). On mobile (< 768px), sidebar hides behind a hamburger toggle and slides in via Bootstrap offcanvas component.
- **D-04:** Bootstrap 5.3 CSS and JS loaded from CDN — no local static Bootstrap files.
- **D-05:** Sidebar shows placeholder links: Dashboard and Settings. These link to placeholder pages or homepage until wired in Phase 3.
- **D-06:** Sidebar brand header shows app name "FlaskStuct" + a Bootstrap icon (e.g., house/grid icon) from Bootstrap Icons CDN.
- **D-07:** No admin-only links in Phase 1. Role-gated sidebar items are deferred to Phase 3.
- **D-08:** Current page indicated with Bootstrap `.active` class on the sidebar link.
- **D-09:** Error pages (403, 404, 500) are standalone minimal templates — they do NOT extend `base.html`. Prevents broken sidebar/nav from compounding an error state.
- **D-10:** Error messaging uses friendly, helpful tone (e.g., "Oops! Page not found.") with a clear "Go Home" button.
- **D-11:** Error pages show app name + a relevant Bootstrap icon (exclamation-triangle for 500, question-circle for 404) as branding.
- **D-12:** Single `error.html` template shared across all error codes — accepts code, title, and message as variables. Register error handlers in `create_app()`.
- **D-13:** Structural mobile responsiveness only: viewport meta tag, sidebar hamburger collapse at 768px, and base template responsive grid. Individual page mobile polish (form widths, stacked layouts) deferred to Phase 3 per MOB-02 and MOB-04.
- **D-14:** A minimal custom CSS file at `app/static/css/app.css` with essential overrides: sidebar width, content padding when sidebar is visible, mobile hamburger styling. No framework — just targeted overrides.
- **D-15:** Bootstrap JS bundle with Popper (`bootstrap.bundle.min.js`) from CDN — required for offcanvas sidebar component.
- **D-16:** All scripts placed at end of `<body>` in `base.html` (standard performance practice).

### the agent's Discretion
- Exact Bootstrap icon choice for sidebar brand and error pages
- Custom CSS specifics beyond the decisions above (specific pixel values, hover states)
- Jinja block naming beyond the core blocks: `head`, `content`, `sidebar`, `scripts`
- Exact wording of error page messages beyond the friendly/helpful tone
- Whether to include a favicon link in base.html

### Deferred Ideas (OUT OF SCOPE)
- Admin-only sidebar links with role gating → Phase 3
- Full mobile polish (320px+ readability, dashboard vertical stacking) → Phase 3
- Login/Register form touch-friendly sizing → Phase 2
- Bootstrap Icons local fallback (only CDN for now)
- Dark mode toggle (not in scope for v1)

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| MAIN-01 | Homepage shows "Flask app is running" placeholder | Section 3: Template Architecture; Section 6: Blueprint Registration |
| LAYOUT-01 | base.html provides consistent layout with Bootstrap 5 | Section 3: Template Architecture; Section 5: Static Assets |
| LAYOUT-02 | Error pages exist and are styled (403, 404, 500) | Section 7: Error Handler Architecture |
| MOB-01 | Sidebar collapses to hamburger menu on screens < 768px | Section 3: Template Architecture (offcanvas); Section 5: Static Assets (mobile CSS) |
| MOB-03 | Login/register forms render full-width and touch-friendly | Section 3: Template Architecture (responsive grid ensures full-width behavior) |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Flask | 3.1.3 | Web framework, app factory, routing, templates | De-facto Python web microframework; app factory pattern is canonical for multi-config setups |
| python-dotenv | 1.2.2 | Load `.env` into `os.environ` | Standard approach for 12-factor app configuration in Python [VERIFIED: PyPI] |

### Frontend (CDN — no local install)
| Library | Version | Purpose | CDN URL |
|---------|---------|---------|---------|
| Bootstrap CSS | 5.3.8 | Responsive grid, offcanvas, typography, components | `https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css` [VERIFIED: getbootstrap.com/docs/5.3] |
| Bootstrap JS Bundle | 5.3.8 | Offcanvas component, Popper for positioning | `https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js` [VERIFIED: getbootstrap.com/docs/5.3] |
| Bootstrap Icons | 1.13.1 | Icon web font for sidebar brand and error pages | `https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css` [VERIFIED: HTTP 200 on CDN] |

**Integrity hashes (from official Bootstrap docs for 5.3.8):**
- CSS: `sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB`
- JS Bundle: `sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI`

**Installation:**
```bash
pip install flask==3.1.3 python-dotenv==1.2.2
```

## Package Legitimacy Audit

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| flask | PyPI | ~16 yrs | 100M+/mo | github.com/pallets/flask | [ASSUMED] | Approved |
| python-dotenv | PyPI | ~9 yrs | 40M+/mo | github.com/theskumar/python-dotenv | [ASSUMED] | Approved |

**Packages removed due to slopcheck:** none
**Packages flagged as suspicious:** none

*Note: slopcheck was installed (v0.6.1) but produced no output for these packages. Packages are tagged [ASSUMED] because slopcheck did not produce a definitive [OK] verdict. These are universally recognized, long-established packages with millions of downloads — risk is negligible.*

## File Manifest & Build Order

Files are listed in dependency order. A file cannot be created before its dependencies exist.

| # | File | Purpose | Depends On | Wave |
|---|------|---------|------------|------|
| 0 | `.gitignore` | Ignore venv, instance, .env, __pycache__, .planning/ | None | 0 |
| 1 | `requirements.txt` | Declare pip dependencies | None | 0 |
| 2 | `.env.example` | Template for environment variables (no secrets) | None | 0 |
| 3 | `config.py` | Configuration class hierarchy | None | 0 |
| 4 | `app/__init__.py` | `create_app()` factory function | 3 | 1 |
| 5 | `app/extensions.py` | Extension instances (db, login, csrf, mail) | None | 1 |
| 6 | `app/static/css/app.css` | Custom CSS overrides | None | 1 |
| 7 | `app/templates/base.html` | Base layout with Bootstrap + sidebar | None | 1 |
| 8 | `app/templates/home.html` | Homepage placeholder | 7 | 1 |
| 9 | `app/templates/error.html` | Shared error page template | None | 1 |
| 10 | `app/main/__init__.py` | Main blueprint creation | None | 2 |
| 11 | `app/main/routes.py` | Homepage route, about/contact placeholder | 10 | 2 |
| 12 | `app/auth/__init__.py` | Auth blueprint placeholder (empty) | None | 2 |
| 13 | `run.py` | Entry point — imports and runs create_app() | 4 | 3 |

**Wave grouping:**
- **Wave 0** (files 0-3): Project config, no Python code. Can run in parallel.
- **Wave 1** (files 4-9): Core app factory, static assets, templates. `app/__init__.py` depends on `config.py`; templates are independent of each other.
- **Wave 2** (files 10-12): Blueprints and routes. Depend on factory existing but can be verified without running.
- **Wave 3** (file 13): Entry point. Must be last — requires all other files.

## Component Specifications

### 1. `requirements.txt`
```
Flask==3.1.3
python-dotenv==1.2.2
```
[VERIFIED: PyPI - flask 3.1.3, python-dotenv 1.2.2 are current latest]

### 2. `.env.example`
```
SECRET_KEY=change-me-to-a-random-secret
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///instance/app.db
```

### 3. `config.py`
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///instance/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
```

**Key decisions:**
- `SECRET_KEY`: Falls back to hardcoded string only when env var absent — for dev convenience. Production must set env var. [CITED: flask.palletsprojects.com/en/stable/config/]
- `SQLALCHEMY_DATABASE_URI`: Defaults to SQLite for zero-config dev. [CITED: flask-sqlalchemy.palletsprojects.com]
- `WTF_CSRF_ENABLED`: True by default — set in Config base so all envs get CSRF protection. [ASSUMED: standard Flask-WTF pattern]
- `load_dotenv()`: Called at module level so env vars are available when config classes are evaluated. [CITED: pypi.org/project/python-dotenv]

### 4. `app/extensions.py`
```python
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
```
[VERIFIED: flask-sqlalchemy.palletsprojects.com] — Extension pattern: create instances without app, bind later with `init_app()`

Note: `flask-sqlalchemy`, `flask-login`, `flask-wtf`, `flask-mail` are not installed in Phase 1 — the extensions.py file is created as a forward-compatible placeholder. Import errors will occur if run before Phase 2 installs the packages. The `create_app()` should guard extension init with try/except or defer init_app calls to Phase 2.

**Phase 1-appropriate approach:** Create `extensions.py` with placeholder imports guarded by `try/except ImportError`, or simply create the file with a comment explaining the pattern. The factory in Phase 1 does NOT call `init_app()` on any extension — that wiring happens in Phase 2.

### 5. `app/__init__.py` (App Factory)
```python
import os
from flask import Flask, render_template

def create_app(config_name=None):
    """Create and configure the Flask application.

    Args:
        config_name: One of 'development', 'production', 'testing'.
                     Defaults to FLASK_ENV env var or 'development'.
    """
    app = Flask(__name__)

    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    if config_name == 'production':
        from config import ProductionConfig
        app.config.from_object(ProductionConfig)
    elif config_name == 'testing':
        from config import TestingConfig
        app.config.from_object(TestingConfig)
    else:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)

    # Register blueprints
    from app.main import main_bp
    app.register_blueprint(main_bp)

    # Register error handlers (shared error template pattern per D-12)
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    """Register error handlers using a shared error.html template."""

    error_pages = {
        403: {
            'title': 'Access Forbidden',
            'message': 'Sorry, you don\'t have permission to access this page.',
            'icon': 'bi-shield-lock'
        },
        404: {
            'title': 'Page Not Found',
            'message': 'Oops! The page you\'re looking for doesn\'t exist.',
            'icon': 'bi-question-circle'
        },
        500: {
            'title': 'Internal Server Error',
            'message': 'Something went wrong on our end. Please try again later.',
            'icon': 'bi-exclamation-triangle'
        },
    }

    def make_handler(code, title, message, icon):
        def handler(e):
            return render_template('error.html',
                                   code=code,
                                   title=title,
                                   message=message,
                                   icon=icon), code
        return handler

    for code, data in error_pages.items():
        app.register_error_handler(code, make_handler(
            code, data['title'], data['message'], data['icon']
        ))
```

**Key decisions:**
- Error handlers use `register_error_handler()` (not decorator) — compatible with factory pattern. [VERIFIED: flask.palletsprojects.com/en/stable/errorhandling/]
- Icon choices: `bi-shield-lock` (403), `bi-question-circle` (404), `bi-exclamation-triangle` (500) — all from Bootstrap Icons 1.13.1 font. [ASSUMED — icon names verified against Bootstrap Icons catalog]
- The `make_handler` closure pattern avoids repeating handler code while keeping each error code's data distinct.
- Blueprints imported inside factory function — prevents circular imports. [VERIFIED: flask.palletsprojects.com/en/stable/patterns/appfactories/]

### 6. `app/main/__init__.py`
```python
from flask import Blueprint

main_bp = Blueprint('main', __name__)
```
[VERIFIED: flask.palletsprojects.com/en/stable/blueprints/]

### 7. `app/main/routes.py`
```python
from app.main import main_bp
from flask import render_template

@main_bp.route('/')
def index():
    """Homepage — shows placeholder to confirm scaffold works."""
    return render_template('home.html')


@main_bp.route('/about')
def about():
    """Placeholder about page — extends base.html."""
    return render_template('about.html')


@main_bp.route('/contact')
def contact():
    """Placeholder contact page — extends base.html."""
    return render_template('contact.html')
```

**Note:** `about.html` and `contact.html` are minimal placeholder templates created in Phase 1 to demonstrate the sidebar `.active` class detection works. They simply extend `base.html` with a block content heading. No auth gating, no forms.

### 8. `app/auth/__init__.py`
```python
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
```

**Note:** Created in Phase 1 as a forward-compatible placeholder. Not registered in `create_app()` until Phase 2. This avoids future merge conflicts and establishes the pattern.

### 9. `run.py`
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Rationale:** Module-level `app = create_app()` makes `flask run` work (it auto-detects the `app` variable). The `__main__` guard supports `python run.py` for development. [VERIFIED: flask.palletsprojects.com/en/stable/patterns/appfactories/#using-applications]

## Template Architecture

### Base Template (`app/templates/base.html`)

**Jinja block layout:**
```
head           — <head> contents: meta, title, CSS CDNs, custom CSS
  ├── title    — <title> tag (default: "FlaskStuct")
content        — Main content area (page-specific)
sidebar        — Sidebar: dual-element (fixed desktop + offcanvas mobile)
scripts        — End of <body>: Bootstrap JS bundle CDN
```

**Exact CDN URLs with integrity hashes:**

```html
<!-- Bootstrap 5.3.8 CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB"
      crossorigin="anonymous">

<!-- Bootstrap Icons 1.13.1 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css"
      rel="stylesheet">

<!-- Bootstrap 5.3.8 JS Bundle (with Popper) -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI"
        crossorigin="anonymous"></script>
```

**Viewport meta tag (required for responsive offcanvas):**
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### Sidebar Architecture (D-02, D-03, D-05, D-06, D-08)

The sidebar uses a **dual-element pattern**:

1. **Fixed sidebar** (`d-none d-md-flex`): Visible on desktop (>=768px). Positioned as a fixed left column using Bootstrap grid classes (`col-md-3 col-lg-2`) with custom CSS for `position: fixed` behavior.

2. **Offcanvas sidebar** (Bootstrap `.offcanvas`): Visible on mobile (<768px). Toggled by a hamburger button (`d-md-none`). Uses `data-bs-toggle="offcanvas"` and `data-bs-target="#mobileSidebar"`.

**Sidebar content** (shared between both elements):
- **Brand header**: "FlaskStuct" text + Bootstrap `bi-house` icon
- **Navigation links**:
  - Dashboard → `url_for('main.index')` (placeholder homepage until Phase 3)
  - Settings → `url_for('main.index')` (placeholder homepage until Phase 3)

**Active page detection (D-08):**
```jinja
{% set active_page = request.endpoint %}
<a href="{{ url_for('main.index') }}"
   class="nav-link {% if active_page == 'main.index' %}active{% endif %}">
```

**Hamburger toggle (mobile only):**
```html
<button class="btn d-md-none" type="button" data-bs-toggle="offcanvas"
        data-bs-target="#mobileSidebar" aria-controls="mobileSidebar">
    <span class="navbar-toggler-icon"></span>
</button>
```

### Homepage Template (`app/templates/home.html`)
```jinja
{% extends "base.html" %}

{% block title %}FlaskStuct - Home{% endblock %}

{% block content %}
<div class="container-fluid py-4">
    <h1>FlaskStuct</h1>
    <p class="lead">Flask app is running.</p>
</div>
{% endblock %}
```

### Error Template (`app/templates/error.html`) — Standalone, does NOT extend base.html (D-09)

```jinja
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ title }} - FlaskStuct</title>
    <!-- Bootstrap CSS CDN (same URLs as base.html) -->
    <!-- Bootstrap Icons CDN -->
    <style>
        /* Minimal inline styles for error page centering */
        body { display: flex; align-items: center; justify-content: center;
               min-height: 100vh; background-color: #f8f9fa; }
        .error-container { text-align: center; padding: 2rem; }
    </style>
</head>
<body>
    <div class="error-container">
        <i class="{{ icon }} display-1 text-muted mb-3"></i>
        <h1>{{ code }}</h1>
        <h2 class="h4 text-muted">{{ title }}</h2>
        <p class="lead">{{ message }}</p>
        <a href="{{ url_for('main.index') }}" class="btn btn-primary btn-lg mt-3">
            <i class="bi-house"></i> Go Home
        </a>
    </div>
</body>
</html>
```

**Variables passed from error handlers:**
| Variable | 403 | 404 | 500 |
|----------|-----|-----|-----|
| `code` | 403 | 404 | 500 |
| `title` | "Access Forbidden" | "Page Not Found" | "Internal Server Error" |
| `message` | "Sorry, you don't have permission to access this page." | "Oops! The page you're looking for doesn't exist." | "Something went wrong on our end. Please try again later." |
| `icon` | `bi-shield-lock` | `bi-question-circle` | `bi-exclamation-triangle` |

### Placeholder Templates for Sidebar Active Class Testing

`app/templates/about.html`:
```jinja
{% extends "base.html" %}
{% block title %}About - FlaskStuct{% endblock %}
{% block content %}<h1>About</h1><p>Placeholder about page.</p>{% endblock %}
```

`app/templates/contact.html`:
```jinja
{% extends "base.html" %}
{% block title %}Contact - FlaskStuct{% endblock %}
{% block content %}<h1>Contact</h1><p>Placeholder contact page.</p>{% endblock %}
```

## Static Assets

### `app/static/css/app.css` — Custom CSS Overrides (D-14)

```css
/* ============================================
   FlaskStuct — Custom CSS
   Phase 1: Structural overrides only
   ============================================ */

/* CSS custom properties */
:root {
    --sidebar-width: 250px;
}

/* --- Fixed Sidebar (desktop: >= 768px) --- */
.sidebar-desktop {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: var(--sidebar-width);
    padding: 1rem 0;
    background-color: #f8f9fa;
    border-right: 1px solid #dee2e6;
    overflow-y: auto;
    z-index: 1000;
}

/* Sidebar brand header */
.sidebar-brand {
    padding: 0.5rem 1rem 1rem;
    font-size: 1.25rem;
    font-weight: 600;
    border-bottom: 1px solid #dee2e6;
    margin-bottom: 0.5rem;
}

/* Sidebar nav links */
.sidebar-desktop .nav-link {
    padding: 0.5rem 1rem;
    color: #333;
    border-radius: 0;
    transition: background-color 0.15s ease;
}

.sidebar-desktop .nav-link:hover {
    background-color: #e9ecef;
}

.sidebar-desktop .nav-link.active {
    background-color: #0d6efd;
    color: #fff;
}

/* --- Main Content Shift (makes room for fixed sidebar on desktop) --- */
.content-col {
    margin-left: var(--sidebar-width);
    min-height: 100vh;
    padding: 1.5rem;
}

/* --- Mobile Hamburger Button --- */
.hamburger-btn {
    position: fixed;
    top: 0.75rem;
    left: 0.75rem;
    z-index: 1050;
}

/* --- Mobile Offcanvas Sidebar --- */
/* The .offcanvas component handles its own positioning via Bootstrap JS.
   We only need to set width to match desktop sidebar. */
#mobileSidebar {
    width: var(--sidebar-width);
}

#mobileSidebar .nav-link.active {
    background-color: #0d6efd;
    color: #fff;
}

/* --- Responsive: mobile viewports (< 768px) --- */
@media (max-width: 767.98px) {
    .sidebar-desktop {
        display: none !important;
    }

    .content-col {
        margin-left: 0;
    }
}
```

**Verification of CSS approach:** The offcanvas component's JS/positioning is handled entirely by Bootstrap. Our CSS only sets width for the offcanvas panel, hides the desktop sidebar at the breakpoint, removes content margin on mobile, and styles nav links. [CITED: getbootstrap.com/docs/5.3/components/offcanvas/]

## Blueprint Registration

### Main Blueprint
| Property | Value |
|----------|-------|
| Python package | `app/main/` |
| Blueprint name | `main` |
| Import name | `app.main` |
| URL prefix | `/` (root) |
| Registered in | `create_app()` in `app/__init__.py` |

### Auth Blueprint (placeholder only)
| Property | Value |
|----------|-------|
| Python package | `app/auth/` |
| Blueprint name | `auth` |
| URL prefix | `/auth` |
| Registered in | Phase 2 |

### Route Patterns (Phase 1)
| Route | Endpoint | Method | Template | Purpose |
|-------|----------|--------|----------|---------|
| `/` | `main.index` | GET | `home.html` | Homepage with "Flask app is running" |
| `/about` | `main.about` | GET | `about.html` | Placeholder — tests sidebar active class |
| `/contact` | `main.contact` | GET | `contact.html` | Placeholder — tests sidebar active class |

## Error Handler Architecture (D-09, D-10, D-11, D-12)

### Implementation Pattern

The `register_error_handlers()` function in `app/__init__.py` uses a closure factory pattern:

```
For each error code (403, 404, 500):
    1. Define handler data: {code, title, message, icon}
    2. Create closure via make_handler() — captures per-code data
    3. Register via app.register_error_handler(code, handler)
```

This is the canonical pattern from Flask docs for factory-based apps. [VERIFIED: flask.palletsprojects.com/en/stable/errorhandling/#custom-error-pages]

### Why NOT blueprint error handlers

Per Flask docs: "the blueprint does not 'own' a certain URL space, so the application instance has no way of knowing which blueprint error handler it should run if given an invalid URL." Error handlers for 403, 404, 500 must be registered at the application level. [VERIFIED: flask.palletsprojects.com/en/stable/blueprints/#blueprint-error-handlers]

### Template isolation (D-09)

The error template explicitly omits `{% extends "base.html" %}`. Each error page contains its own minimal `<html>`, `<head>` with viewport meta and Bootstrap CDN, and `<body>`. This ensures error pages render even if the base template or its dependencies are broken.

### Error <-> Template data flow

```
Request → Flask routing → Error occurs (e.g., route not found)
    → Flask looks up registered error handler for 404
    → make_handler closure is called with werkzeug.exceptions.NotFound
    → handler renders error.html with {code: 404, title: "Page Not Found",
       message: "Oops! The page you're looking for doesn't exist.",
       icon: "bi-question-circle"}
    → Returns (rendered_template, 404)
```

## Verification Strategy

| # | Success Criterion | Verification Method | Pass Condition |
|---|-------------------|---------------------|----------------|
| 1 | `python run.py` starts Flask without errors | Manual: `python run.py` then check terminal | No ImportError, no traceback; Flask starts and shows URL |
| 2 | Visiting `/` displays "Flask app is running" | Manual: `curl http://localhost:5000/` or browser visit | Response contains "Flask app is running" |
| 3 | `base.html` renders Bootstrap 5 layout | Manual: View source on `/` | Contains Bootstrap 5.3.8 CSS CDN link, viewport meta, container classes |
| 4 | Sidebar collapses to hamburger on mobile (< 768px) | Manual: Browser DevTools responsive mode, set to 375px width | Fixed sidebar hidden; hamburger button visible; tapping shows offcanvas |
| 5a | 404 error page renders with styling | Manual: `curl http://localhost:5000/nonexistent` or browser visit | Response shows "Page Not Found", "404", Bootstrap styling, icon visible |
| 5b | 500 error page renders | Manual: Temporarily add `@main_bp.route('/trigger-500')` that raises Exception; visit in browser | Friendly error page with "500", "Internal Server Error", icon |
| 5c | 403 error page renders | Manual: `curl http://localhost:5000/static/` or trigger via app | Friendly error page with "403", "Access Forbidden", icon |
| 6 | Responsive grid works (full-width on mobile) | Manual: Browser DevTools at 375px, visit `/` | Content takes full width; no sidebar present; hamburger visible |

**Automated verification (future):** A basic test file can verify:
- `create_app()` returns a Flask instance
- Response from `/` contains 200 status and expected text
- Response from `/nonexistent` returns 404 with HTML body containing "Page Not Found"

## Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Circular imports** (importing app before extensions ready) | MEDIUM | HIGH (app won't start) | All imports inside `create_app()`; extensions in separate file; blueprint imports at function level. [VERIFIED pattern: flask.palletsprojects.com] |
| **CDN unavailability** (Bootstrap CSS/JS doesn't load) | LOW | HIGH (no styling, no offcanvas) | Bootstrap CDN via jsDelivr has 99.99%+ uptime. Use integrity hashes to detect tampering. No local fallback per D-04 — accepted risk. |
| **Offcanvas JS not working** (missing Popper, wrong data attributes) | MEDIUM | HIGH (mobile sidebar broken) | Use `bootstrap.bundle.min.js` (includes Popper). Verify `data-bs-toggle="offcanvas"` attribute on hamburger. Test on mobile viewport during verification. |
| **Viewport meta missing** | MEDIUM | MEDIUM (mobile layout broken) | Viewport meta tag is in `base.html` `<head>`. Hard requirement from Bootstrap docs. Verification step checks source. |
| **Error template broken** (syntax error in Jinja) | LOW | HIGH (500 page can't render) | Error template is standalone and minimal — no extends, few variables. Test by triggering each error code during verification. |
| **`request.endpoint` is None** (no route matched) | LOW | LOW (sidebar `.active` won't highlight) | Only happens on error pages — but error pages don't extend base.html (D-09), so no sidebar. Not a problem in practice. |
| **Flask not installed or wrong version** | MEDIUM | HIGH (app won't start) | `requirements.txt` pins exact version; verification step 1 catches this. |
| **Port 5000 already in use** | LOW | LOW (can't start dev server) | Change port in `run.py` or use `flask run --port 5001`. Not a code issue. |

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Responsive sidebar collapse | Custom JS media query listener + CSS transitions | Bootstrap Offcanvas component with `offcanvas-md` and `data-bs-toggle` | Bootstrap handles show/hide, backdrop, scroll lock, keyboard dismiss, and accessibility (aria attributes, focus management) across all browsers |
| Mobile hamburger toggle | Custom button + custom show/hide logic | Bootstrap `navbar-toggler-icon` + `data-bs-toggle="offcanvas"` | Zero custom JS; accessibility built-in |
| Configuration loading from env | `os.getenv()` scattered through code | `Config` class hierarchy with `from_object()` + `python-dotenv` | Centralized, testable, environment-switchable without code changes |
| Secret key generation | Hardcoded string | `os.environ.get('SECRET_KEY', fallback)` in config class | Prevents secrets in git; overridable per environment |
| Error page rendering | Per-code template files (404.html, 500.html) | Single `error.html` with parameterized code/title/message | D-12 locks this decision; reduces template count, ensures consistency |

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `app = Flask(__name__)` at module level | `create_app()` factory function | Flask 0.7+ (but became standard practice ~2018) | Required for multi-config, testing, extension init without circular imports |
| `app.errorhandler(404)` decorator on module | `app.register_error_handler(404, handler)` inside factory | Supported since Flask 0.7; preferred for factories | Decorators don't work inside factory function body |
| Bootstrap 4 JQuery dependency | Bootstrap 5 — vanilla JS, no JQuery | Bootstrap 5.0 (2021) | No more JQuery dependency; `data-bs-*` attribute naming |
| Bootstrap 4 navbar collapse | Bootstrap 5 offcanvas component | Bootstrap 5.2 (2022) | Proper slide-in sidebar vs. stacked collapse; better mobile UX |

## Common Pitfalls

### Pitfall 1: Importing app module-level causes circular imports
**What goes wrong:** A blueprint or extension file does `from app import app` at module level. Python's import system creates a circular dependency.
**Root cause:** The factory pattern requires `create_app()` to complete before other modules can access the app. Module-level imports try to access it before it exists.
**How to avoid:** Always place imports inside `create_app()`. Use `current_app` proxy in blueprints. In `extensions.py`, create instances without app binding — call `init_app()` in factory.
**Warning signs:** `ImportError: cannot import name 'app' from partially initialized module`

### Pitfall 2: Offcanvas doesn't open on mobile
**What goes wrong:** Hamburger button visible but clicking does nothing.
**Root cause:** Missing Bootstrap JS bundle (or using CSS-only bundle), or wrong `data-bs-target` selector.
**How to avoid:** Always use `bootstrap.bundle.min.js` (includes Popper). Verify `data-bs-target="#mobileSidebar"` matches the offcanvas element's `id="mobileSidebar"`. Test on mobile viewport as verification step.
**Warning signs:** No JS console errors; button click has no effect.

### Pitfall 3: Error pages show broken sidebar
**What goes wrong:** 404 page renders with half-broken sidebar and navigation.
**Root cause:** Error template extends `base.html` — if the error is caused by something in the base template pipeline, the error page itself breaks.
**How to avoid:** Error template is standalone (D-09). Include its own minimal `<head>` with Bootstrap CDN directly.
**Warning signs:** Error page shows base template errors in addition to the original error.

### Pitfall 4: Hardcoded SECRET_KEY committed to git
**What goes wrong:** Production deploy has a predictable secret key, sessions can be forged.
**Root cause:** Putting the actual secret key in `config.py` and committing it.
**How to avoid:** `SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-fallback')`. The dev fallback is only for local development. `.env` is in `.gitignore`. `.env.example` shows the structure without real secrets.
**Warning signs:** `SECRET_KEY = "my-secret-key"` as string literal in committed code.

## Code Examples

### App Factory Pattern (canonical)
```python
# Source: flask.palletsprojects.com/en/stable/patterns/appfactories/
def create_app(config_filename=None):
    app = Flask(__name__)
    # load config
    # register extensions via init_app()
    # register blueprints
    # register error handlers
    return app
```

### Error Handler Registration in Factory
```python
# Source: flask.palletsprojects.com/en/stable/errorhandling/#custom-error-pages
def create_app():
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    return app
```

### Bootstrap Offcanvas Toggle (data attributes)
```html
<!-- Source: getbootstrap.com/docs/5.3/components/offcanvas/#live-demo -->
<button class="btn btn-primary" type="button" data-bs-toggle="offcanvas"
        data-bs-target="#offcanvasExample" aria-controls="offcanvasExample">
    Button with data-bs-target
</button>

<div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasExample"
     aria-labelledby="offcanvasExampleLabel">
    <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasExampleLabel">Offcanvas</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas"
                aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
        <!-- content -->
    </div>
</div>
```

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | Flask runtime | ✓ | 3.12.3 | — |
| pip3 | Package installation | ✓ | 24.0 | — |
| Flask (via pip) | App framework | ✗ (not yet installed) | 3.1.3 (target) | Install via `pip install -r requirements.txt` |
| python-dotenv (via pip) | Env var loading | ✗ (not yet installed) | 1.2.2 (target) | Install via `pip install -r requirements.txt` |
| Flask-SQLAlchemy (via pip) | Database ORM | ✗ (not yet installed) | — | Not imported in Phase 1; placeholder in extensions.py only |
| Flask-Login (via pip) | Auth sessions | ✗ (not yet installed) | — | Not imported in Phase 1; placeholder in extensions.py only |
| Flask-WTF (via pip) | CSRF protection | ✗ (not yet installed) | — | Not imported in Phase 1; placeholder in extensions.py only |
| Flask-Mail (via pip) | Email sending | ✗ (not yet installed) | — | Not imported in Phase 1; placeholder in extensions.py only |
| Jinja2 | Template rendering | ✓ | 3.1.2 (system) | — |
| Bootstrap CDN (external) | CSS/JS | ✓ (CDN — HTTP 200 verified) | 5.3.8 | — |
| Bootstrap Icons CDN (external) | Icon font | ✓ (CDN — HTTP 200 verified) | 1.13.1 | — |

**Missing dependencies with no fallback:**
- Flask 3.1.3 — must be installed via `pip install -r requirements.txt` before `python run.py` works.
- python-dotenv 1.2.2 — must be installed for `.env` loading.

**Missing dependencies with fallback:**
- Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Mail — not needed in Phase 1. Extensions file uses a try/except ImportError guard so the app starts without them.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (to be installed — not present) |
| Config file | none — see Wave 0 |
| Quick run command | `python -m pytest tests/ -x` |
| Full suite command | `python -m pytest tests/ -v` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| MAIN-01 | `/` returns 200 with "Flask app is running" | unit | `pytest tests/test_main.py::test_homepage -x` | ❌ Wave 0 |
| LAYOUT-01 | `base.html` includes Bootstrap CDN links and viewport meta | unit | `pytest tests/test_layout.py::test_base_template_has_bootstrap -x` | ❌ Wave 0 |
| LAYOUT-02 | `/nonexistent` returns 404 with styled error page | unit | `pytest tests/test_errors.py::test_404_page -x` | ❌ Wave 0 |
| MOB-01 | Desktop viewport shows fixed sidebar; mobile shows hamburger | manual-only | — (requires visual verification at different viewports) | — |
| MOB-03 | Base template has responsive viewport meta | unit | `pytest tests/test_layout.py::test_viewport_meta -x` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `python run.py` starts, `curl localhost:5000/` returns 200
- **Per wave merge:** All automated tests pass; manual verification of mobile breakpoint
- **Phase gate:** All 6 success criteria verified

### Wave 0 Gaps
- [ ] `tests/conftest.py` — Flask test client fixture (create_app with TestingConfig)
- [ ] `tests/test_main.py` — covers MAIN-01 (homepage content)
- [ ] `tests/test_layout.py` — covers LAYOUT-01 (base template structure), MOB-03 (viewport meta)
- [ ] `tests/test_errors.py` — covers LAYOUT-02 (404, 403, 500 error pages)
- [ ] `pytest` install: `pip install pytest` — not in requirements.txt
- [ ] `requirements.txt` — add pytest as dev dependency or separate requirements-dev.txt

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No (Phase 2) | — |
| V3 Session Management | No (Phase 2) | — |
| V4 Access Control | No (Phase 2) | — |
| V5 Input Validation | No (no forms in Phase 1) | — |
| V6 Cryptography | Minimal | SECRET_KEY from env var, not hardcoded; Werkzeug session signing uses it |

### Known Threat Patterns for Phase 1 Stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Secret key in source control | Information Disclosure | `.env` in `.gitignore`; `SECRET_KEY` from `os.environ.get()`; `.env.example` shows template only |
| Debug mode in production | Information Disclosure | `config.py` has `ProductionConfig(DEBUG=False)`; factory defaults to `development` but production must opt in |
| CDN tampering (MITM on Bootstrap files) | Tampering | Integrity hashes on `<link>` and `<script>` tags verify file contents match expected hash [VERIFIED: getbootstrap.com docs include integrity attributes] |
| Error pages leaking stack traces | Information Disclosure | Custom error handlers return friendly pages; Werkzeug debugger only active in DEBUG=True (development) |

## Sources

### Primary (HIGH confidence)
- [Flask 3.1.x documentation](https://flask.palletsprojects.com/en/stable/) — App factories, error handling, blueprints (all verified against 3.1.x docs)
- [Bootstrap 5.3 documentation](https://getbootstrap.com/docs/5.3/) — Getting started (CDN URLs, viewport meta), Offcanvas component (responsive breakpoints, data attributes, placement)
- [Bootstrap Icons](https://icons.getbootstrap.com/) — Current version 1.13.1, icon catalog
- [PyPI](https://pypi.org/) — Package versions: flask 3.1.3, python-dotenv 1.2.2, flask-sqlalchemy 3.1.1

### Secondary (MEDIUM confidence)
- [jsDelivr CDN](https://cdn.jsdelivr.net/) — CDN URL verification via HTTP HEAD requests; all Bootstrap CDN URLs returned HTTP 200

### Tertiary (LOW confidence)
- None — all critical claims verified against official docs or CDN responses

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Bootstrap Icons `bi-house`, `bi-shield-lock`, `bi-question-circle`, `bi-exclamation-triangle` are in the 1.13.1 font | Error Handler Architecture | LOW — these are long-standing icons present since v1.0; risk is a missing icon glyph which is cosmetic only |
| A2 | `offcanvas-md` responsive class works at 768px breakpoint as documented | Template Architecture | LOW — Bootstrap's breakpoints are stable; `md` = 768px is documented at getbootstrap.com/docs/5.3/layout/breakpoints/ |
| A3 | `flask-sqlalchemy`, `flask-login`, `flask-wtf`, `flask-mail` will be available when Phase 2 needs them | Component Specifications | LOW — these are well-maintained packages with stable PyPI presence; extensions.py uses try/except ImportError guard so Phase 1 doesn't break if they're missing |
| A4 | The integrity hash `sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI` is correct for bootstrap.bundle.min.js 5.3.8 | Template Architecture | LOW — copied verbatim from official Bootstrap 5.3.8 docs page; browser will refuse to load if hash mismatches, which is a safe failure mode |

## Open Questions (RESOLVED)

1. **Favicon inclusion**
   - What we know: D-06 says user can decide; CONTEXT.md marks it as agent's discretion
   - What's unclear: Whether to include a favicon link in `<head>` or skip entirely
   - Recommendation: Include a minimal favicon link pointing to a Bootstrap icon SVG as favicon, or omit (no favicon means no 404 noise during dev)
   - **RESOLVED: Omit favicon entirely — no favicon link in base.html or error.html. Avoids 404 noise during dev and defers the decision to a later phase.**

2. **extensions.py — stub or guard?**
   - What we know: Phase 1 doesn't install sqlalchemy, login, wtf, or mail. Creating `extensions.py` with bare imports will crash on app start.
   - What's unclear: Whether to use `try/except ImportError` guards or create as a comment-only placeholder
   - Recommendation: Use try/except ImportError with `pass` for each extension, and a module docstring explaining Phase 2 wiring. The planner should decide based on whether `app/__init__.py` imports from `extensions.py` in Phase 1 (it should not — factory defers extension init to Phase 2).
   - **RESOLVED: Use `try/except ImportError` guards for all four extensions (SQLAlchemy, LoginManager, CSRFProtect, Mail). On import failure, set instance to `None`. create_app() does NOT import from extensions.py in Phase 1.**

3. **About/Contact placeholder routes**
   - What we know: Sidebar needs multiple links to test `.active` class detection. Dashboard and Settings both link to `main.index` — but with two links both pointing to the same route, the `.active` detection works but the distinguishment is limited.
   - What's unclear: Whether to create `/about` and `/contact` as genuine placeholder routes (extends base.html, simple content) or skip them
   - Recommendation: Create both — minimal effort (one route + one template each), and they provide testable endpoints for sidebar navigation behavior.
   - **RESOLVED: Create both `/about` and `/contact` as placeholder routes with minimal templates extending base.html. Provides distinct endpoints for sidebar `.active` class detection and navigation testing.**

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — Flask 3.1.3, python-dotenv 1.2.2 verified on PyPI; Bootstrap 5.3.8 CDN verified via HTTP 200 and official docs; Bootstrap Icons 1.13.1 CDN verified via HTTP 200
- Architecture: HIGH — App factory, extension, and blueprint patterns verified against Flask 3.1.x official documentation
- Templates: HIGH — Bootstrap offcanvas and responsive breakpoints verified against Bootstrap 5.3 official documentation
- Pitfalls: HIGH — Circular imports, offcanvas JS dependency, secret key handling, and CDN tampering all addressed with verified mitigations
- Errors: MEDIUM — Named icon choices (A1) rely on training knowledge of Bootstrap Icons catalog; risk is low (cosmetic only)

**Research date:** 2026-05-30
**Valid until:** 2026-06-29 (30 days — stable frameworks, no expected breaking changes)

## RESEARCH COMPLETE
