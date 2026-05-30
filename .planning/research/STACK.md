# Stack Research: Flask Scaffold

## Recommended Stack

| Layer | Choice | Version | Rationale | Confidence |
|-------|--------|---------|-----------|------------|
| **Framework** | Flask | 3.1+ | Lightweight, mature, perfect for modular scaffolds | High |
| **ORM** | Flask-SQLAlchemy | 3.1+ | Standard ORM for Flask, migration path to Postgres/MySQL via connection string only | High |
| **Auth/Sessions** | Flask-Login | 0.6+ | De-facto session management, `current_user`, `login_required` | High |
| **Forms** | Flask-WTF | 1.2+ | CSRF built-in, WTForms integration, validation | High |
| **Password Hashing** | Werkzeug | 3.1+ | Ships with Flask, `generate_password_hash` / `check_password_hash` | High |
| **Password Reset Tokens** | itsdangerous | 2.2+ | Ships with Flask, timed serializer for reset tokens | High |
| **Email (prototype)** | Flask-Mail | 0.10+ | Standard, swap SMTP config later | Medium |
| **CSS Framework** | Bootstrap 5 | 5.3 | Mobile-first, navbar/offcanvas components, no JS framework needed | High |
| **Environment Config** | python-dotenv | 1.0+ | Load `.env` for secrets, standard pattern | High |

## NOT using

| Avoid | Why |
|-------|-----|
| **Flask-Security / Flask-Security-Too** | Over-engineered for this scaffold; hides auth internals we want visible for expansion |
| **Django** | Too opinionated; user chose Flask explicitly |
| **FastAPI** | Async-first, different paradigm; not what user asked for |
| **Celery** | Overkill for password reset emails at prototype stage |
| **HTMX** | Adds JS dependency; user wants pure server-rendered |

## Database Strategy

- **Prototype:** SQLite (`sqlite:///instance/app.db`) — zero config
- **Production:** PostgreSQL or MySQL — swap `SQLALCHEMY_DATABASE_URI` in config only
- **Migration:** Flask-Migrate (Alembic) can be added later when schema evolves beyond initial models
