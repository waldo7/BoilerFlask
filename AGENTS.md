# AGENTS.md — FlaskStuct

## Project
- **Name:** FlaskStuct
- **Repo:** `flaskstuct/`
- **Stack:** Flask 3.1+, Jinja, Bootstrap 5, SQLAlchemy (SQLite dev, Postgres/MySQL prod)
- **Planning:** `.planning/` — PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md

## Commands
```bash
# Start dev server (Windows PowerShell)
.\venv\Scripts\python run.py

# Start dev server (Bash / WSL)
./venv/bin/python run.py

# Install dependencies (Windows PowerShell)
.\venv\Scripts\pip install -r requirements.txt

# Install dependencies (Bash / WSL)
./venv/bin/pip install -r requirements.txt

# Run tests (from Windows PowerShell via WSL)
wsl ./venv/bin/python -m pytest
```

## Core Value
Developers get a production-ready, organized Flask foundation with auth and responsive UI out of the box.

## Active Phase
◆ Phase 3: Dashboard & Sidebar — Active (planning phase)

## Key Architecture Rules
- App factory pattern: `create_app()` in `app/__init__.py`
- Extensions initialized in `extensions.py` — never import app directly
- Blueprints per domain (main/, auth/)
- Jinja template inheritance from `base.html`
- Config via classes in `config.py`, secrets from environment vars
