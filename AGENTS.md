# AGENTS.md — FlaskStuct

## Project
- **Name:** FlaskStuct
- **Repo:** `flaskstuct/`
- **Stack:** Flask 3.1+, Jinja, Bootstrap 5, SQLAlchemy (SQLite dev, Postgres/MySQL prod)
- **Planning:** `.planning/` — PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md

## Commands
```bash
# Start dev server
python run.py

# Install dependencies
pip install -r requirements.txt
```

## Core Value
Developers get a production-ready, organized Flask foundation with auth and responsive UI out of the box.

## Active Phase
○ None — project just initialized. Run `/gsd-plan-phase 1` to begin.

## Key Architecture Rules
- App factory pattern: `create_app()` in `app/__init__.py`
- Extensions initialized in `extensions.py` — never import app directly
- Blueprints per domain (main/, auth/)
- Jinja template inheritance from `base.html`
- Config via classes in `config.py`, secrets from environment vars
