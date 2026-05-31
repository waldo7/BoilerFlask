"""BoilerFlask — Extension instances.

Created without app binding to prevent circular imports.
Extension init_app() calls are wired in create_app() (Phase 2).
"""

# ---------------------------------------------------------------------------
# SQLAlchemy — database ORM
# ---------------------------------------------------------------------------
try:
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()
except ImportError:
    db = None

# ---------------------------------------------------------------------------
# Flask-Login — user session management
# ---------------------------------------------------------------------------
try:
    from flask_login import LoginManager
    login_manager = LoginManager()
except ImportError:
    login_manager = None

# ---------------------------------------------------------------------------
# Flask-WTF CSRF — cross-site request forgery protection
# ---------------------------------------------------------------------------
try:
    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect()
except ImportError:
    csrf = None

# ---------------------------------------------------------------------------
# Flask-Mail — email sending support
# ---------------------------------------------------------------------------
try:
    from flask_mail import Mail
    mail = Mail()
except ImportError:
    mail = None
