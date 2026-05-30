# Pitfalls Research: Flask Scaffold

## Pitfall 1: Circular Imports

**Warning signs:** `ImportError`, app won't start, models not found
**Prevention:**
- Separate `extensions.py` — init extensions without app, call `init_app(app)` in factory
- Never import `app` from other modules; use `current_app` proxy
- Blueprints import models at function level (inside routes), not module level
**Phase to address:** Phase 1 (critical to get right from start)

## Pitfall 2: No Password Hashing

**Warning signs:** Plaintext passwords in DB — catastrophic security hole
**Prevention:**
- Use `werkzeug.security.generate_password_hash()` in User model setter
- Use `werkzeug.security.check_password_hash()` in login verification
- Never store or log raw passwords
**Phase to address:** Phase 2 (auth system)

## Pitfall 3: CSRF on Login Forms

**Warning signs:** Login fails with 400 after deployment
**Prevention:**
- Flask-WTF enables CSRF globally via `CSRFProtect(app)`
- Always include `{{ form.hidden_tag() }}` in Jinja forms
- Test login/logout flows with CSRF enabled early
**Phase to address:** Phase 2

## Pitfall 4: Session Not Persistent

**Warning signs:** User logged out after browser close or server restart
**Prevention:**
- Set `app.config['REMEMBER_COOKIE_DURATION']` for "remember me"
- Use `login_user(user, remember=True)` for persistent sessions
- SQLite: sessions survive restart; production: configure server-side sessions
**Phase to address:** Phase 2

## Pitfall 5: Mobile Nav Not Working

**Warning signs:** Sidebar covers content on mobile, hamburger unresponsive
**Prevention:**
- Bootstrap offcanvas for mobile sidebar (not just CSS hide/show)
- Include Bootstrap JS bundle (needed for offcanvas toggle)
- Test at 320px, 375px, 768px viewports
- Ensure `viewport` meta tag in `<head>`
**Phase to address:** Phase 1 and Phase 3

## Pitfall 6: Hardcoded Config

**Warning signs:** Credentials committed to git, different envs break
**Prevention:**
- `config.py` with `Config` base class, `DevelopmentConfig`, `ProductionConfig`
- `SECRET_KEY` from `os.environ.get()` with fallback for dev
- `SQLALCHEMY_DATABASE_URI` from env or default to SQLite
- Never commit secrets
**Phase to address:** Phase 1

## Pitfall 7: Missing Error Handlers

**Warning signs:** Ugly Werkzeug debug pages in production, no 404 styling
**Prevention:**
- Register error handlers in `create_app()`: `@app.errorhandler(404)`
- Create `errors/` template directory with styled pages
- Wrap with `base.html` or minimal layout for errors
**Phase to address:** Phase 1
