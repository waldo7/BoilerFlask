# Phase 2: Auth System — Research

**Researched:** 2026-05-30
**Domain:** Flask authentication (registration, login, logout, password reset, role-based authorization)
**Confidence:** HIGH

## Summary

Phase 2 delivers complete Flask authentication using the standard Pallets-eco stack: Flask-SQLAlchemy (ORM), Flask-Login (session management), Flask-WTF (CSRF + form validation), Flask-Mail (email), Flask-Migrate (Alembic migrations), and Flask-Limiter (rate limiting). All libraries are mature (5–15+ years), well-maintained, and slopcheck-verified clean.

The auth pages use a standalone `auth/base.html` shell (not extending the main `base.html`), consistent with the Phase 1 `error.html` standalone precedent. The User model lives at `app/models/user.py` with a three-tier role enum (`admin`/`superuser`/`user`). Password reset uses itsdangerous `URLSafeTimedSerializer` with 1-hour expiry and one-time-use enforcement via DB tracking. Development prints reset URLs to console; production sends real SMTP emails.

The primary integration risk is `create_app()` wiring: all four extensions (`db`, `login_manager`, `csrf`, `mail`) must be `init_app()`-ed, plus `login_manager.user_loader` callback registration, `login_manager.login_view` assignment, and `auth_bp` blueprint registration. No circular import hazards exist — the `extensions.py` pattern from Phase 1 handles this.

**Primary recommendation:** Wire extensions and `user_loader` in `create_app()` first (dependency for all other tasks), build the User model second, then auth routes/forms/templates in parallel waves.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| User model + persistence | Database / Storage | — | SQLAlchemy ORM, single source of truth |
| Session management | API / Backend | Browser (cookies) | Flask-Login manages server-side sessions; browser stores cookies |
| CSRF protection | API / Backend | Browser (forms) | Flask-WTF generates tokens server-side; browser embeds via `hidden_tag()` |
| Form validation | API / Backend | Browser (display) | WTForms validates server-side; errors rendered client-side |
| Password hashing | API / Backend | — | Werkzeug `generate_password_hash` / `check_password_hash` |
| Password reset tokens | API / Backend | — | itsdangerous TimedSerializer generates signed tokens |
| Rate limiting | API / Backend | — | Flask-Limiter middleware counts requests server-side |
| Email sending | API / Backend | SMTP | Flask-Mail sends via SMTP in prod; console in dev |
| Auth page rendering | Frontend Server (SSR) | — | Jinja templates rendered server-side, no client JS |
| Login redirect flow | API / Backend | Browser | Flask-Login handles `next` query param redirects |
| Admin CLI commands | API / Backend (CLI) | — | Flask CLI custom commands via `@app.cli.command` |
| Dashboard stub | Frontend Server (SSR) | API (auth gate) | `@login_required` decorator gates access |

## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Auth pages use a standalone `auth/base.html` shell — NOT extending `base.html`. Consistent with `error.html` standalone precedent (Phase 1 D-09). No sidebar, no desktop nav.
- **D-02:** Auth shell layout: vertically/horizontally centered card + FlaskStuct brand header at top + "Back to Home" link below.
- **D-03:** Single `app/templates/auth/base.html` with `auth_content` Jinja block. Login, register, forgot-password, reset-password all extend this. Located at `app/templates/auth/` directory.
- **D-04:** Auth pages cross-link: register page shows "Already have an account? Log in", login shows "No account? Register", forgot-password shows "Remembered? Log in".
- **D-05:** Token-based reset using itsdangerous TimedSerializer. DevelopmentConfig prints token/reset URL to console (no email sent). ProductionConfig sends real email via Flask-Mail with SMTP env vars. Both paths exist in the code — config determines which activates.
- **D-06:** After submitting forgot-password form: show generic "If that email exists, we sent a reset link" page. Same message regardless of whether email address was found — prevents user enumeration.
- **D-07:** Reset tokens: 1-hour expiry, one-time use (deleted/invalidated after successful password change). TimedSerializer handles expiry, DB tracking handles one-time enforcement.
- **D-08:** After successful password reset: redirect to /auth/login with "Password reset successfully. Please log in." flash message. No auto-login after reset.
- **D-09:** Registration always assigns `user` role. No role selector on the registration form — prevents privilege escalation.
- **D-10:** Admin creation via Flask CLI commands: `flask create-admin` (creates new admin user) and `flask set-admin` (promotes existing user to any role). Password input uses `getpass` for hidden input (Django createsuperuser pattern).
- **D-11:** Three-tier role enum in User model: `admin`, `superuser`, `user`. All three exist from day one. `user` is default on registration. `superuser` created/promoted via CLI only in Phase 2. Role-gated sidebar items and admin panel for role management deferred to Phase 3/v2 (ADMN-01/02/03).
- **D-12:** Login form includes "Remember me" checkbox.
- **D-13:** "Remember me" checked → 30-day persistent session. Unchecked → session cookie expires on browser close.
- **D-14:** Expired/missing session on protected page → redirect to /auth/login with flash "Please log in to continue." + save original URL via `next` query parameter.
- **D-15:** Secure cookie defaults in Config base class: `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE='Lax'`, `REMEMBER_COOKIE_HTTPONLY=True`. ProductionConfig sets `SESSION_COOKIE_SECURE=True`.
- **D-16:** After login → redirect to `/dashboard` (minimal stub route created in Phase 2; enhanced in Phase 3).
- **D-17:** After registration → auto-login + redirect to `/dashboard` stub. User must not re-enter credentials.
- **D-18:** After logout → redirect to `/` (homepage).
- **D-19:** Unauthenticated access to protected page → save original URL via `next` query param. After login, redirect back to original URL. Falls back to `/dashboard` if no `next` present.
- **D-20:** Minimum 8 characters, at least 2 of 4 character types (uppercase, lowercase, digit, symbol).
- **D-21:** Confirm password field on registration and password reset forms. Passwords must match.
- **D-22:** Show/hide password toggle on password fields using Bootstrap eye icon (requires Bootstrap JS — already loaded from CDN in Phase 1).
- **D-23:** Form validation errors displayed inline per-field (WTForms default) + summary alert banner at top for server-side errors (email taken, invalid credentials).
- **D-24:** User model columns: `id` (PK, auto-increment), `email` (unique, indexed), `password_hash`, `role` (enum: admin/superuser/user), `created_at`, `updated_at`, `is_active` (boolean, default True).
- **D-25:** `is_active=False` prevents login AND invalidates existing sessions. Checked in `@login_manager.user_loader` — if user is deactivated while logged in, session is terminated on next request.
- **D-26:** User model lives at `app/models/user.py` per ARCHITECTURE.md. `app/models/__init__.py` imports User for clean imports elsewhere.
- **D-27:** Emails normalized at registration and login: lowercase + whitespace stripped. Stored case-insensitively to prevent duplicate accounts.
- **D-28:** Duplicate email prevention: DB `unique=True` constraint + WTForms validator checking for existing normalized email. Gives friendly "Email already registered" form error instead of raw DB integrity error.
- **D-29:** Flask-Limiter dependency added for rate limiting. Applied to all auth POST endpoints: `/auth/login`, `/auth/register`, `/auth/forgot-password`, `/auth/reset-password`.
- **D-30:** Default limit: 10 requests per minute per IP address. Configurable via config.py (`RATELIMIT_DEFAULT` and per-route decorators).
- **D-31:** Rate limit exceeded → flash message "Too many attempts. Please try again in X seconds." and form is re-rendered. Not a separate 429 error page.
- **D-32:** Flask-Migrate (Alembic) added as dependency. Commands: `flask db init`, `flask db migrate -m "message"`, `flask db upgrade`.
- **D-33:** Development helper: in `DevelopmentConfig`, if tables don't exist on startup, call `db.create_all()` for zero-friction first-run. Production always requires explicit `flask db upgrade`.

### the agent's Discretion
- Exact Bootstrap icon choices for auth shell and form toggles
- Specific CSS for auth card centering, form width, and spacing
- WTForms field labels and placeholder text wording
- Flash message category styling (success/error/warning)
- Whether to use WTForms `Email` + `PasswordField` or plain `StringField` with validators
- Exact `itsdangerous` serializer salt string

### Deferred Ideas (OUT OF SCOPE)
- Admin user management panel (role assignment UI, user listing) → Phase 3 / v2 (ADMN-01/02/03)
- Superuser role UI for admin panel → Phase 3 / v2
- Dark mode toggle → future
- Display name and last_login fields on User model → developers add when forking
- OAuth / social login (Google, GitHub) → v2 (AUTH-08)
- Email verification flow → v2 (AUTH-07)
- User profile editing → v2 (AUTH-09)
- Avatar uploads → v2 (FEAT-01)

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| AUTH-01 | User can register with email and password | RegistrationForm (Flask-WTF), User model (Flask-SQLAlchemy), werkzeug hashing, email normalization |
| AUTH-02 | User can log in and session persists across browser refresh | Flask-Login `login_user()` with `remember=True`, `REMEMBER_COOKIE_DURATION=30 days`, `current_user` proxy |
| AUTH-03 | User can log out from any page | Flask-Login `logout_user()`, logout route at `/auth/logout`, redirect to `/` |
| AUTH-04 | User can request password reset via email | itsdangerous URLSafeTimedSerializer, Flask-Mail (prod), console print (dev), forgot-password + reset-password flows |
| AUTH-05 | User has a role (admin/user) assigned | Three-tier role enum in User model, `user` default on registration, Flask CLI `create-admin`/`set-admin` for role promotion |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Flask-SQLAlchemy | 3.1.1 | ORM + DB session management | Pallets-eco blessed, ties SQLAlchemy sessions to Flask request lifecycle [VERIFIED: PyPI] |
| Flask-Login | 0.6.3 | User session management | De facto Flask auth session library — `login_user()`, `logout_user()`, `@login_required`, `current_user` [VERIFIED: PyPI] |
| Flask-WTF | 1.3.0 | CSRF protection + form validation | Built-in CSRF via `CSRFProtect()`, WTForms integration, `FlaskForm.validate_on_submit()` [VERIFIED: PyPI] |
| Werkzeug | 3.1.8 | Password hashing | Ships with Flask — `generate_password_hash()`/`check_password_hash()`, zero extra deps [VERIFIED: PyPI] |
| itsdangerous | 2.2.0 | Password reset tokens | Ships with Flask — `URLSafeTimedSerializer` for signed, time-limited tokens [VERIFIED: PyPI] |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Flask-Mail | 0.10.0 | SMTP email sending | Production email delivery; dev mode prints to console via D-05 [VERIFIED: PyPI] |
| Flask-Migrate | 4.1.0 | Alembic DB migrations | Schema evolution — `flask db init/migrate/upgrade`; auto-enables `compare_type=True` and `render_as_batch=True` for SQLite [VERIFIED: PyPI] |
| Flask-Limiter | 4.1.1 | Rate limiting | POST endpoint protection — 10 req/min/IP default, memory:// storage in dev [VERIFIED: PyPI] |
| email-validator | 2.3.0 | Email validation | WTForms `Email()` validator backend; RFC-compliant email check [VERIFIED: PyPI] |
| Alembic | 1.18.4 | Migration engine | Pulled in by Flask-Migrate; auto-generates upgrade/downgrade scripts [VERIFIED: PyPI] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Flask-Login | Flask-Security-Too | Over-engineered for scaffold; hides auth internals; harder to fork and extend per user's intent |
| Werkzeug hashing | bcrypt | Extra dependency for same security level; Werkzeug ships with Flask |
| itsdangerous | PyJWT | itsdangerous is simpler for single-token reset flows; no key rotation overhead needed |
| Flask-Mail | smtplib directly | Flask-Mail provides `MAIL_SUPPRESS_SEND` for testing, `Message` abstraction, signal support |
| Flask-Limiter | Wrote custom rate limiter | Flask-Limiter handles storage backends, key functions, decorators; hand-rolling risks subtle race conditions |

**Installation:**
```bash
pip install Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Flask-WTF==1.3.0 \
            Flask-Mail==0.10.0 Flask-Migrate==4.1.0 Flask-Limiter==4.1.1 \
            email-validator==2.3.0
```

## Package Legitimacy Audit

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| flask-sqlalchemy | PyPI | 15+ yrs | High (ecosystem standard) | github.com/pallets-eco/flask-sqlalchemy | [OK] | Approved |
| flask-login | PyPI | 12+ yrs | High (ecosystem standard) | github.com/maxcountryman/flask-login | [OK] | Approved |
| flask-wtf | PyPI | 14+ yrs | High (ecosystem standard) | github.com/pallets-eco/flask-wtf | [OK] | Approved |
| flask-mail | PyPI | 12+ yrs | High (ecosystem standard) | github.com/pallets-eco/flask-mail | [OK] | Approved |
| flask-migrate | PyPI | 10+ yrs | High (ecosystem standard) | github.com/miguelgrinberg/flask-migrate | [OK] | Approved |
| flask-limiter | PyPI | 10+ yrs | High (ecosystem standard) | github.com/alisaifee/flask-limiter | [OK] | Approved |
| email-validator | PyPI | 7+ yrs | High (ecosystem standard) | github.com/JoshData/python-email-validator | [OK] | Approved |

**Packages removed due to slopcheck [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

All seven packages verified clean by slopcheck on PyPI. All are well-established ecosystem standards with active maintenance. No postinstall script concerns apply (Python packages).

## Architecture Patterns

### System Architecture Diagram

```
┌──────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│ Browser  │────▶│ Flask WSGI App       │────▶│ SQLite / PostgreSQL  │
│          │◀────│                      │◀────│                     │
└──────────┘     └──────┬───────────────┘     └─────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
   ┌──────────┐  ┌───────────┐  ┌───────────┐
   │Flask-    │  │Flask-WTF  │  │Flask-     │
   │Login     │  │(CSRF,     │  │Limiter    │
   │(session) │  │ forms)    │  │(rate      │
   └──────────┘  └───────────┘  │limit)     │
                                └───────────┘
   ┌──────────────────────────────────────┐
   │           Auth Flow                  │
   │                                      │
   │  GET /auth/login                     │
   │    └─▶ Render login.html             │
   │  POST /auth/login                    │
   │    ├─▶ Rate limit check              │
   │    ├─▶ CSRF validation               │
   │    ├─▶ Form validation (WTForms)     │
   │    ├─▶ User query (normalized email) │
   │    ├─▶ Password verify (werkzeug)    │
   │    ├─▶ is_active check               │
   │    ├─▶ login_user(remember=...)      │
   │    └─▶ Redirect to next or dashboard │
   │                                      │
   │  GET /auth/register                  │
   │    └─▶ Render register.html          │
   │  POST /auth/register                 │
   │    ├─▶ Rate limit check              │
   │    ├─▶ Form validation               │
   │    ├─▶ Duplicate email check         │
   │    ├─▶ Create User (role=user)       │
   │    ├─▶ Auto-login                    │
   │    └─▶ Redirect /dashboard           │
   │                                      │
   │  POST /auth/forgot-password          │
   │    ├─▶ Rate limit check              │
   │    ├─▶ Lookup normalized email       │
   │    ├─▶ Generate TimedSerializer token│
   │    ├─▶ Dev: print to console         │
   │    ├─▶ Prod: send email via SMTP     │
   │    └─▶ Render "check email" page     │
   │                                      │
   │  GET /auth/reset-password/<token>    │
   │    ├─▶ Verify token (TimedSerializer)│
   │    ├─▶ Check DB (not used yet)       │
   │    └─▶ Render reset-password form    │
   │  POST /auth/reset-password/<token>   │
   │    ├─▶ Verify token                  │
   │    ├─▶ Update password_hash          │
   │    ├─▶ Mark token as used (DB)       │
   │    └─▶ Flash + redirect to login     │
   └──────────────────────────────────────┘
```

### Recommended Project Structure
```
app/
├── __init__.py          # create_app() — extension wiring, blueprint registration
├── extensions.py        # db, login_manager, csrf, mail (Phase 1 — NO changes needed)
├── config.py            # NEW config keys for MAIL_*, RATELIMIT_*, REMEMBER_COOKIE_*
├── models/
│   ├── __init__.py      # NEW — imports User for clean access
│   └── user.py          # NEW — User model with UserMixin
├── auth/
│   ├── __init__.py      # MODIFY — auth_bp import (Phase 1 exist; add routes import)
│   ├── routes.py        # NEW — all auth route handlers
│   └── forms.py         # NEW — LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm
├── main/
│   ├── __init__.py      # Phase 1 — NO changes
│   └── routes.py        # MODIFY — add /dashboard stub route
├── templates/
│   ├── base.html        # Phase 1 — NO changes (auth pages don't extend this)
│   ├── auth/
│   │   ├── base.html    # NEW — standalone auth shell
│   │   ├── login.html   # NEW — login form
│   │   ├── register.html # NEW — registration form
│   │   ├── forgot_password.html  # NEW — forgot password form
│   │   ├── reset_password.html   # NEW — reset password form
│   │   └── reset_request_sent.html # NEW — confirmation after forgot-password submit
│   └── dashboard.html   # NEW — minimal stub (extends base.html)
├── static/
│   └── css/
│       └── app.css      # MODIFY — add auth form centering/card styles
└── commands.py           # NEW — Flask CLI: create-admin, set-admin
```

### Pattern 1: App Factory Extension Wiring
**What:** Extensions created in `extensions.py` (no app binding) are wired to the app in `create_app()` via `init_app()`.
**When to use:** Every phase that adds extensions. Phase 2 wires all four.
**Example:**
```python
# Source: flask-login.readthedocs.io/en/latest/
# app/__init__.py — inside create_app()
from app.extensions import db, login_manager, csrf, mail
from app.models.user import User

# Wire extensions
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)
mail.init_app(app)

# Flask-Login configuration
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to continue.'
login_manager.login_message_category = 'warning'

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
from app.auth import auth_bp
app.register_blueprint(auth_bp)
```

### Pattern 2: Flask-SQLAlchemy User Model with Flask-Login
**What:** Model inherits from `db.Model` and `UserMixin`, providing Flask-Login interface.
**When to use:** User model definition.
**Example:**
```python
# Source: flask-sqlalchemy.readthedocs.io/en/stable/ + flask-login.readthedocs.io/en/latest/
# app/models/user.py
from datetime import datetime, timezone
from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class Role(enum.Enum):
    USER = 'user'
    ADMIN = 'admin'
    SUPERUSER = 'superuser'

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Role), default=Role.USER, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'
```

### Pattern 3: Flask-WTF Form with Custom Validators
**What:** `FlaskForm` subclass with WTForms fields and validators, including custom email-uniqueness check.
**When to use:** All auth forms.
**Example:**
```python
# Source: flask-wtf.readthedocs.io/en/latest/quickstart/
# app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters.')
    ])
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])

    def validate_email(self, field):
        # Normalize + check uniqueness
        email = field.data.strip().lower()
        if User.query.filter_by(email=email).first():
            raise ValidationError('Email already registered.')
```

### Pattern 4: Rate-Limited Auth Route with Flask-Limiter
**What:** Rate limit decorator on POST handlers with custom breach handling for flash messages.
**When to use:** All auth POST endpoints (login, register, forgot-password, reset-password).
**Example:**
```python
# Source: flask-limiter.readthedocs.io/en/stable/
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    default_limits=["10 per minute"],
    storage_uri="memory://",
)

# On route:
@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login_post():
    # ...
```

### Pattern 5: itsdangerous Timed Password Reset Token
**What:** `URLSafeTimedSerializer` signs a user ID with salt, generating time-limited URL-safe tokens.
**When to use:** Forgot-password flow.
**Example:**
```python
# Source: itsdangerous.palletsprojects.com/en/stable/
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app

def generate_reset_token(user):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(str(user.id), salt='password-reset')

def verify_reset_token(token, max_age=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token, salt='password-reset', max_age=max_age)
    except SignatureExpired:
        return None  # Token expired
    except BadSignature:
        return None  # Token invalid
    return User.query.get(int(user_id))
```

### Pattern 6: Blueprint route import pattern
**What:** `app/auth/__init__.py` imports `routes` after blueprint creation to avoid circular imports.
**When to use:** Blueprint route registration pattern.
**Example:**
```python
# Source: Phase 1 pattern from app/main/__init__.py (D-01-CONTEXT)
# app/auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

from app.auth import routes  # noqa: F401 — registers routes on the blueprint
```

### Anti-Patterns to Avoid
- **Importing User model at module level in `app/__init__.py` before `db.init_app(app)`:** The model inherits from `db.Model` which needs the app context. Import inside `create_app()` after `db.init_app(app)`.
- **Using `Email()` validator without `email-validator` installed:** WTForms `Email()` validator requires the `email-validator` package. Without it, validation silently passes all inputs. Always include in `requirements.txt`.
- **Using `url_for('auth.login')` before registering `auth_bp`:** Flask resolves endpoints at runtime, but if the blueprint isn't registered, the URL won't resolve. Register blueprint before referencing it.
- **Not normalizing email case on login:** User registered as `User@Example.com` should be able to log in with `user@example.com`. Always `strip().lower()` on both registration and login.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Session management | Custom cookie/session code | Flask-Login | Handles "remember me" cookies, session expiry, `current_user` proxy, `@login_required` decorator, fresh login tracking, session protection — all edge cases solved |
| CSRF protection | Custom token generation + validation | Flask-WTF `CSRFProtect` | Handles token generation, per-form tokens, exempt routing, AJAX support, error customization — subtle bypass vectors if hand-rolled |
| Password hashing | Custom hash/salt | Werkzeug `generate_password_hash` / `check_password_hash` | Uses industry-standard algorithm (pbkdf2:sha256 by default), handles salt generation, upgrade path to new algorithms |
| Signed tokens (reset) | Custom HMAC + timestamp | itsdangerous `URLSafeTimedSerializer` | URL-safe encoding, timestamp verification, signature validation, key rotation support — one `loads()` call handles expiry + tampering |
| Rate limiting | Custom request counting | Flask-Limiter | Storage backends (memory, Redis, memcached), sliding/fixed window strategies, per-route customization, exemption filters — race condition handling is non-trivial |
| Form validation | Manual request.form parsing | Flask-WTF + WTForms | Built-in validators (Length, Email, EqualTo, custom), error rendering, CSRF integration, `validate_on_submit()` — writing manual validators risks injection |
| DB migrations | Manual ALTER TABLE scripts | Flask-Migrate (Alembic) | Auto-generation from model diffs, upgrade/downgrade, history tracking, batch mode for SQLite ALTER limitations — manual scripts diverge from models |

**Key insight:** Each of these problems has 10+ years of community experience baked into the standard library. Hand-rolling any of them takes more code, more bugs, and more maintenance than using the standard library — and the standard library is already in the stack.

## Common Pitfalls

### Pitfall 1: User Model Imported Before db.init_app()
**What goes wrong:** `ImportError` or runtime `RuntimeError: application not registered on db instance` when importing User model at module level in `app/__init__.py` before `db.init_app(app)` is called.
**Why it happens:** The User model inherits from `db.Model`. `db` is a `SQLAlchemy()` instance that hasn't been bound to an app yet. Importing the model class triggers metaclass registration that needs the app context.
**How to avoid:** Import the User model inside `create_app()` AFTER `db.init_app(app)`. Specifically, import in the `@login_manager.user_loader` callback body or at the function level inside `create_app()`.
**Warning signs:** `RuntimeError` at import time; app won't start.

### Pitfall 2: Flask-Login 0.6.3 vs 0.7.0 API Discrepancy
**What goes wrong:** Documentation at flask-login.readthedocs.io shows version 0.7.0 API, but PyPI distributes 0.6.3. API differences (if any) could break code written against docs.
**Why it happens:** ReadTheDocs builds from the `main` branch, which may be ahead of the latest PyPI release.
**How to avoid:** Pin to `Flask-Login==0.6.3` in `requirements.txt`. Verify `LoginManager`, `login_user()`, `logout_user()`, `UserMixin`, `@login_required` APIs by testing early. The core API (these five surfaces) has been stable since 0.4.x — risk is low.
**Warning signs:** AttributeError on `LoginManager` or `UserMixin` methods. Test login flow immediately after installing.

### Pitfall 3: CSRF Token Missing from Non-WTForms Pages
**What goes wrong:** 400 Bad Request on pages that don't use Flask-WTF `FlaskForm` but still POST to the app.
**Why it happens:** `CSRFProtect(app)` enables global CSRF checking. Any POST request without a valid CSRF token gets rejected. If a page uses a plain HTML `<form>` instead of WTForms, the token won't be included.
**How to avoid:** All auth POST forms use `FlaskForm` (which auto-includes CSRF token). Always include `{{ form.hidden_tag() }}` in Jinja templates. Non-auth POST endpoints can use `@csrf.exempt` if needed. Phase 2 auth forms are all WTForms-based, so this is low risk.
**Warning signs:** 400 errors on POST, "The CSRF token is missing" in response.

### Pitfall 4: SQLite ALTER TABLE Limitations
**What goes wrong:** Adding columns or constraints to existing SQLite tables fails because SQLite has limited ALTER TABLE support.
**Why it happens:** SQLite doesn't support ALTER COLUMN, DROP COLUMN (before 3.35), or many constraint modifications.
**How to avoid:** Flask-Migrate 4.1+ auto-enables `render_as_batch=True` for SQLite, which uses the batch mode ("move and copy") workaround. This is enabled by default — no configuration needed. The `db.create_all()` fallback in DevelopmentConfig (D-33) means first-run doesn't need migrations at all.
**Warning signs:** "OperationalError: near 'ALTER'" during migration. If seen, verify Flask-Migrate >= 4.0.

### Pitfall 5: Remember Me Cookie Not Persisting
**What goes wrong:** User checks "Remember me" but gets logged out after browser close.
**Why it happens:** Missing `REMEMBER_COOKIE_DURATION` config, or `login_user(user, remember=True)` not using the `remember` parameter from the form.
**How to avoid:** Set `REMEMBER_COOKIE_DURATION = timedelta(days=30)` in Config base class. Pass `remember=form.remember.data` to `login_user()`. Verify `REMEMBER_COOKIE_HTTPONLY=True` is set (already in D-15).
**Warning signs:** Session lost after browser restart despite "Remember me" checked.

### Pitfall 6: Rate Limiter Blocking Tests
**What goes wrong:** Integration tests hitting auth endpoints get 429 errors after a few requests.
**Why it happens:** Default rate limits (10/min) apply to the test client as well. Shared-state storage (memory://) accumulates across test runs if not reset.
**How to avoid:** Either set `RATELIMIT_ENABLED=False` in TestingConfig, or use a separate `Limiter` instance for test config with `storage_uri="memory://"` and call reset between tests. Simpler: disable rate limiting in test config (it's tested manually, not in automated tests).
**Warning signs:** Tests that hit auth endpoints multiple times fail with unexpected 429.

### Pitfall 7: itsdangerous `BadTimeSignature` on Clock Skew
**What goes wrong:** Token valid on one system fails on another due to server clock differences.
**Why it happens:** `TimedSerializer` uses UTC timestamps. If token is generated on a server with a different clock, expiry may trigger prematurely.
**How to avoid:** Always use `datetime.now(timezone.utc)` for the User model's `created_at`/`updated_at`. The `TimestampSigner` in itsdangerous uses `int(time.time())` internally, which is UTC-based. For dev (single machine), this is Not a problem. For prod, use NTP.
**Warning signs:** Tokens expiring immediately after generation; `SignatureExpired` on freshly created tokens.

## Code Examples

Verified patterns from official sources:

### User Loader with is_active Check
```python
# Source: flask-login.readthedocs.io/en/latest/ — user_loader + D-25 requirement
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user is None:
        return None
    if not user.is_active:
        return None  # Terminate session for deactivated users
    return user
```

### Login Route with `next` URL Validation
```python
# Source: flask-login.readthedocs.io/en/latest/ — Login Example + D-14, D-19
from urllib.parse import urlparse, urljoin
from flask import request, redirect, url_for, flash
from flask_login import login_user

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', form=form)
```

### Flask CLI Admin Commands
```python
# Source: Flask docs + D-10 requirement
# app/commands.py
import click
from getpass import getpass
from app import create_app
from app.extensions import db
from app.models.user import User, Role

app = create_app()

@app.cli.command('create-admin')
def create_admin():
    """Create a new admin user interactively."""
    email = input('Email: ').strip().lower()
    password = getpass('Password: ')
    confirm = getpass('Confirm password: ')
    if password != confirm:
        click.echo('Passwords do not match.', err=True)
        return
    with app.app_context():
        if User.query.filter_by(email=email).first():
            click.echo(f'User {email} already exists.', err=True)
            return
        user = User(email=email, role=Role.ADMIN)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    click.echo(f'Admin user {email} created.')

@app.cli.command('set-admin')
@click.argument('email')
@click.option('--role', type=click.Choice(['user', 'admin', 'superuser']), default='admin')
def set_admin(email, role):
    """Promote an existing user to a role."""
    with app.app_context():
        user = User.query.filter_by(email=email.strip().lower()).first()
        if not user:
            click.echo(f'User {email} not found.', err=True)
            return
        user.role = Role(role)
        db.session.commit()
    click.echo(f'User {email} role set to {role}.')
```

### Auth Shell Template (`auth/base.html`)
```jinja
{# Source: D-01, D-02, D-03 — standalone auth layout, Bootstrap 5 #}
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}FlaskStuct{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">
</head>
<body class="min-vh-100 d-flex align-items-center justify-content-center bg-light">
    <div class="auth-container">
        <div class="text-center mb-4">
            <a href="{{ url_for('main.index') }}" class="text-decoration-none">
                <i class="bi bi-house display-6 text-primary"></i>
                <h4 class="mt-2 text-dark">FlaskStuct</h4>
            </a>
        </div>

        {# Flash messages #}
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <div class="card shadow-sm">
            <div class="card-body p-4">
                {% block auth_content %}{% endblock %}
            </div>
        </div>

        <div class="text-center mt-3">
            <a href="{{ url_for('main.index') }}" class="text-muted small">
                <i class="bi bi-arrow-left"></i> Back to Home
            </a>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI"
            crossorigin="anonymous"></script>
</body>
</html>
```

### Flask-Migrate Initialization
```python
# Source: flask-migrate.readthedocs.io/en/latest/ — init_app pattern
from flask_migrate import Migrate
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # ... config loading ...
    db.init_app(app)
    migrate.init_app(app, db)
    # ...
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Flask-SQLAlchemy 2.x `db.Column(db.String)` without type hints | Flask-SQLAlchemy 3.x with full SQLAlchemy 2.0 typing support | 2023 (v3.0) | Type hints on model columns; `db.Column` unchanged but underlying engine modernized |
| Flask-Login manual `is_authenticated` etc. properties | `UserMixin` provides all defaults | Always available | Less boilerplate in User model |
| Flask-WTF 0.x importing from `flask_wtf` | Flask-WTF 1.x — import fields from `wtforms` directly | 2015 (v0.9) | Cleaner separation; no change needed since Phase 1 doesn't exist yet |
| Alembic manual `compare_type=True`, `render_as_batch=True` | Flask-Migrate 4.x auto-enables both | 2023 (v4.0) | Zero-config SQLite migration support |
| Flask-Limiter 3.x `RATELIMIT_HEADERS_ENABLED` | Flask-Limiter 4.x — headers disabled by default; use `RATELIMIT_HEADERS_ENABLED=True` to opt in | 2024 (v4.0) | Cleaner default; Phase 2 doesn't need headers, so no config change needed |

**Deprecated/outdated:**
- **`flask.ext.*` imports:** Removed in Flask 1.0. Use `flask_sqlalchemy`, `flask_login`, etc. Phase 1 already uses this pattern in `extensions.py`.
- **`db.create_all()` in production:** D-32/D-33 explicitly gate this to DevelopmentConfig. Prod must use `flask db upgrade`.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Flask-Login 0.6.3 on PyPI has the same core API (LoginManager, login_user, logout_user, UserMixin, @login_required) as the 0.7.0 docs show | Standard Stack | LOW — core API has been stable since 0.4.x; any change would break the entire Flask ecosystem |
| A2 | Werkzeug 3.1.8 `generate_password_hash` uses pbkdf2:sha256 by default and is suitable for production | Standard Stack | LOW — documented default since Werkzeug 2.x; attack resistance is well-studied |
| A3 | `URLSafeTimedSerializer` (itsdangerous) is the correct choice for password reset URLs vs plain `TimedSerializer` | Architecture Patterns | LOW — URL-safe is explicitly for URL embedding; the docs confirm this use case |
| A4 | WTForms `Email()` validator from `wtforms.validators` requires the `email-validator` package to be installed separately | Common Pitfalls | LOW — verified in official WTForms docs; the error message when missing is clear (`pip install email-validator`) |
| A5 | Flask-Migrate 4.1+ auto-enables `render_as_batch=True` for all databases, not just SQLite | Common Pitfalls | LOW — confirmed in Flask-Migrate 4.0 changelog; batch mode is a no-op on databases that support ALTER TABLE natively |
| A6 | Flask-Limiter default `storage_uri="memory://"` is suitable for development (destroys state on restart) but not production | Environment Availability | LOW — production docs recommend Redis/memcached; Phase 2 explicitly dev-only |

## Open Questions (RESOLVED)

1. **Flask-Login 0.6.3 vs 0.7.0 version gap**
   - What we know: ReadTheDocs builds from main branch (0.7.0-dev), PyPI distributes 0.6.3. Core API identical.
   - What was unclear: When 0.7.0 will be released, if any breaking changes exist.
   - RESOLVED: Pin to 0.6.3, test core API early. No blocking concern.

2. **Flask-Mail SMTP testing without real SMTP server**
   - What we know: `MAIL_SUPPRESS_SEND=True` prevents actual sending. `mail.record_messages()` captures outbound messages in test.
   - What was unclear: Whether `DevelopmentConfig` should use `MAIL_SUPPRESS_SEND=True` + console print, or attempt real SMTP with MailHog/Mailpit.
   - RESOLVED: Follow D-05 exactly — console print in dev, SMTP in prod. `MAIL_SUPPRESS_SEND=False` in dev (we want to test the full code path, output just goes to console). Tests use `MAIL_SUPPRESS_SEND=True`.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.12 | Runtime | ✓ | 3.12.3 | — |
| pip | Package install | ✓ | 24.0 | — |
| Flask | Core framework | ✗ (not in path) | — | Install in venv via `pip install` |
| flask-sqlalchemy | ORM / User model | ✗ | — | Install in venv |
| flask-login | Session management | ✗ | — | Install in venv |
| flask-wtf | CSRF / forms | ✗ | — | Install in venv |
| flask-mail | Email sending | ✗ | — | Install in venv |
| flask-migrate | DB migrations | ✗ | — | Install in venv |
| flask-limiter | Rate limiting | ✗ | — | Install in venv |
| email-validator | Email validation | ✗ | — | Install in venv |
| SQLite | Database (dev) | ✓ | Built-in (stdlib) | — |
| SMTP server | Email (prod only) | ✗ | — | Dev uses console print; prod requires configured SMTP |

**Missing dependencies with no fallback:**
- All Python packages need to be installed in the project venv. The `pip install` command in the Standard Stack section handles this.

**Missing dependencies with fallback:**
- SMTP server: Development uses console print (D-05). Production requires SMTP configuration, documented in `.env.example`.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (already configured in Phase 1) |
| Config file | `conftest.py` — `app` and `client` fixtures use `TestingConfig` |
| Quick run command | `pytest tests/test_auth.py -x` |
| Full suite command | `pytest tests/ -x` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| AUTH-01 | Registration form renders at GET /auth/register | unit | `pytest tests/test_auth.py::test_register_page -x` | ❌ Wave 0 |
| AUTH-01 | POST /auth/register with valid data creates user and redirects | integration | `pytest tests/test_auth.py::test_register_success -x` | ❌ Wave 0 |
| AUTH-01 | POST /auth/register with existing email shows error | integration | `pytest tests/test_auth.py::test_register_duplicate_email -x` | ❌ Wave 0 |
| AUTH-01 | POST /auth/register with weak password shows validation error | unit | `pytest tests/test_auth.py::test_register_weak_password -x` | ❌ Wave 0 |
| AUTH-02 | Login form renders at GET /auth/login | unit | `pytest tests/test_auth.py::test_login_page -x` | ❌ Wave 0 |
| AUTH-02 | POST /auth/login with valid credentials creates session | integration | `pytest tests/test_auth.py::test_login_success -x` | ❌ Wave 0 |
| AUTH-02 | POST /auth/login with "remember me" sets long-lived cookie | integration | `pytest tests/test_auth.py::test_login_remember_me -x` | ❌ Wave 0 |
| AUTH-02 | POST /auth/login with bad credentials shows error | integration | `pytest tests/test_auth.py::test_login_bad_credentials -x` | ❌ Wave 0 |
| AUTH-02 | POST /auth/login with deactivated account is rejected | integration | `pytest tests/test_auth.py::test_login_inactive_user -x` | ❌ Wave 0 |
| AUTH-03 | GET /auth/logout clears session and redirects | integration | `pytest tests/test_auth.py::test_logout -x` | ❌ Wave 0 |
| AUTH-04 | GET /auth/forgot-password renders form | unit | `pytest tests/test_auth.py::test_forgot_password_page -x` | ❌ Wave 0 |
| AUTH-04 | POST /auth/forgot-password shows confirmation page (existing email) | integration | `pytest tests/test_auth.py::test_forgot_password_existing_email -x` | ❌ Wave 0 |
| AUTH-04 | POST /auth/forgot-password shows same confirmation page (non-existent email) | integration | `pytest tests/test_auth.py::test_forgot_password_unknown_email -x` | ❌ Wave 0 |
| AUTH-04 | GET /auth/reset-password/<valid_token> renders reset form | integration | `pytest tests/test_auth.py::test_reset_password_valid_token -x` | ❌ Wave 0 |
| AUTH-04 | GET /auth/reset-password/<expired_token> shows error | integration | `pytest tests/test_auth.py::test_reset_password_expired_token -x` | ❌ Wave 0 |
| AUTH-04 | POST /auth/reset-password/<token> updates password and redirects to login | integration | `pytest tests/test_auth.py::test_reset_password_success -x` | ❌ Wave 0 |
| AUTH-05 | New user created with role=user | unit | `pytest tests/test_auth.py::test_default_role -x` | ❌ Wave 0 |
| AUTH-05 | `flask create-admin` creates user with role=admin | integration | `pytest tests/test_auth.py::test_cli_create_admin -x` | ❌ Wave 0 |
| — | Unauthenticated user accessing /dashboard is redirected to login | integration | `pytest tests/test_auth.py::test_dashboard_redirects_unauthenticated -x` | ❌ Wave 0 |
| — | Invalid/expired session accessing /dashboard redirects with flash message | integration | `pytest tests/test_auth.py::test_expired_session_redirect -x` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `pytest tests/test_auth.py -x` (auth-only, fast)
- **Per wave merge:** `pytest tests/ -x` (full suite, includes Phase 1 tests)
- **Phase gate:** Full suite green before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `tests/test_auth.py` — covers all AUTH-01 through AUTH-05 acceptance tests; does not exist yet
- [ ] `tests/conftest.py` — needs `_db` fixture (SQLite in-memory) and `auth_client` fixture (FlaskLoginClient or manual session setup) for integration tests
- [ ] Framework install: `pip install pytest` — check if already in venv from Phase 1; if not, add to test setup step

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | yes | Flask-Login `@login_required`, Werkzeug `check_password_hash`, `is_active` gate |
| V2.1 Password Security | yes | Werkzeug pbkdf2:sha256 hashing, minimum 8 chars, complexity policy (D-20) |
| V3 Session Management | yes | Flask-Login session cookies, `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE='Lax'`, `REMEMBER_COOKIE_HTTPONLY`, logout clears session |
| V4 Access Control | yes | Role enum on User model, `@login_required` decorator, `is_active` gate (D-25) |
| V5 Input Validation | yes | WTForms validators (DataRequired, Email, Length, EqualTo), custom email uniqueness validator, email-validator for RFC compliance |
| V6 Cryptography | yes | Werkzeug password hashing (no hand-rolled crypto), itsdangerous for signed tokens |
| V7 Error Handling | yes | Generic "check email" message prevents user enumeration (D-06), inline + summary alert errors (D-23) |
| V8 Data Protection | yes | Email normalization prevents duplicate accounts (D-27), `unique=True` DB constraint (D-28) |
| V9 Communications | partial | `SESSION_COOKIE_SECURE=True` in ProductionConfig for HTTPS-only cookies (D-15) |
| V11 Business Logic | yes | Rate limiting on auth endpoints (D-29/D-30), one-time-use tokens (D-07), no role selector on registration (D-09) |

### Known Threat Patterns for Flask Auth

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Brute force login | Elevation of Privilege | Flask-Limiter: 10 req/min/IP on `/auth/login` (D-29/D-30) |
| CSRF on auth forms | Elevation of Privilege | Flask-WTF `CSRFProtect`, `{{ form.hidden_tag() }}` in all forms |
| User enumeration via forgot-password | Information Disclosure | Same response for existing and non-existing emails (D-06) |
| Privilege escalation via role parameter | Elevation of Privilege | No role selector on registration form; role defaults to `user` server-side (D-09) |
| Session fixation | Spoofing | Flask-Login session protection (default: "basic" mode), regenerates session on login |
| Password reset token replay | Elevation of Privilege | One-time-use enforcement via DB tracking (D-07), 1-hour expiry (D-07) |
| Open redirect via `next` parameter | Spoofing | `is_safe_url()` validation — only redirects to same host (D-19) |
| SQL injection | Tampering | SQLAlchemy ORM with parameterized queries — no raw SQL |
| Weak password storage | Information Disclosure | Werkzeug pbkdf2:sha256 with per-password salt — not plaintext, not single-round |
| Cookie theft via XSS | Information Disclosure | `SESSION_COOKIE_HTTPONLY=True`, `REMEMBER_COOKIE_HTTPONLY=True` (D-15) |
| Email injection in from/to fields | Tampering | Flask-Mail `BadHeaderError` on newlines in email fields |

## Sources

### Primary (HIGH confidence)
- [PyPI: flask-sqlalchemy 3.1.1] — `pip index versions flask-sqlalchemy`
- [PyPI: flask-login 0.6.3] — `pip index versions flask-login`
- [PyPI: flask-wtf 1.3.0] — `pip index versions flask-wtf`
- [PyPI: flask-mail 0.10.0] — `pip index versions flask-mail`
- [PyPI: flask-migrate 4.1.0] — `pip index versions flask-migrate`
- [PyPI: flask-limiter 4.1.1] — `pip index versions flask-limiter`
- [PyPI: email-validator 2.3.0] — `pip index versions email-validator`
- [PyPI: itsdangerous 2.2.0] — `pip index versions itsdangerous`
- [PyPI: werkzeug 3.1.8] — `pip index versions werkzeug`
- [PyPI: alembic 1.18.4] — `pip index versions alembic`
- Flask-Login official docs — flask-login.readthedocs.io/en/latest/ (full API reference, LoginManager, login_user, login_required, UserMixin, cookie settings, session protection, automated testing)
- Flask-WTF official docs — flask-wtf.readthedocs.io/en/latest/ (FlaskForm, CSRFProtect, quickstart, form validation)
- Flask-Limiter official docs — flask-limiter.readthedocs.io/en/stable/ (Limiter init, limit decorators, exemption, storage backends, on_breach callbacks)
- Flask-Mail official docs — flask-mail.readthedocs.io/en/latest/ (Mail, Message, MAIL_SUPPRESS_SEND, record_messages, configuration keys)
- Flask-SQLAlchemy official docs — flask-sqlalchemy.readthedocs.io/en/stable/ (init_app, Model, query, configuration)
- Flask-Migrate official docs — flask-migrate.readthedocs.io/en/latest/ (Migrate init, init_app pattern, CLI commands, batch mode)
- itsdangerous official docs — itsdangerous.palletsprojects.com/en/stable/ (URLSafeTimedSerializer, SignatureExpired, BadSignature, salt)

### Secondary (MEDIUM confidence)
- slopcheck 0.6.1 verification — all 7 packages scored [OK] on PyPI
- Phase 1 CONTEXT.md — template patterns, extension wiring precedent, CSS location, blueprint import pattern
- ARCHITECTURE.md — build order, data flow, component boundaries

### Tertiary (LOW confidence)
- None — all findings cross-verified with official sources

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all versions confirmed on PyPI, all packages slopcheck-verified [OK]
- Architecture: HIGH — patterns documented in official Flask ecosystem docs; all verified against existing code
- Pitfalls: HIGH — cross-referenced between official docs, existing PITFALLS.md, and real-world Flask upgrade paths

**Research date:** 2026-05-30
**Valid until:** 2026-07-30 (60 days — stable ecosystem, Flask packages change slowly)

---

## RESEARCH COMPLETE

**Phase:** 2 - Auth System
**Confidence:** HIGH

### Key Findings
1. All 7 required packages verified on PyPI with slopcheck [OK] — no suspicious or slop packages
2. Flask-Login docs show 0.7.0 but PyPI distributes 0.6.3; core API (LoginManager, login_user, UserMixin, @login_required) has been stable since 0.4.x — negligible risk
3. `create_app()` must wire 4 extensions + `user_loader` + `auth_bp` registration — this is the architectural dependency all other tasks depend on
4. Flask-Migrate 4.x auto-enables `render_as_batch=True` for SQLite — zero-config migration support out of the box
5. Rate limiting with Flask-Limiter needs `on_breach` callback for custom flash messages per D-31; otherwise returns generic 429
6. `is_safe_url()` validation on `next` parameter is required to prevent open redirect (D-19) — must be implemented, not skipped
7. TestingConfig should disable rate limiting (`RATELIMIT_ENABLED=False`) to prevent 429 errors in integration tests

### File Created
`.planning/phases/02-auth-system/02-RESEARCH.md`

### Confidence Assessment
| Area | Level | Reason |
|------|-------|--------|
| Standard Stack | HIGH | All versions confirmed on PyPI; slopcheck verified; official docs cross-referenced |
| Architecture | HIGH | Patterns from official Flask docs verified against Phase 1 code patterns |
| Pitfalls | HIGH | Cross-referenced PITFALLS.md, official docs, and real-world Flask upgrade paths |

### Open Questions (RESOLVED)
1. Flask-Login 0.6.3/0.7.0 version gap — RESOLVED: pin to 0.6.3, test early
2. Dev email strategy — RESOLVED: D-05 dictates console print; D-33 dictates `db.create_all()` fallback

### Ready for Planning
Research complete. Planner can now create PLAN.md files. Key architecture decisions are locked in CONTEXT.md; all package versions verified; integration points documented.
