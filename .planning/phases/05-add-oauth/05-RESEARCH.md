# Phase 05: Add OAuth - Research

## Objective
Research how to implement Phase 05: add-oauth using Flask-Dance, SQLAlchemy, and Flask-Login in the FlaskStuct project.

## Flask-Dance Architecture
Flask-Dance provides out-of-the-box Blueprints for popular OAuth providers (Google, GitHub).
The standard setup for integrating Flask-Dance with SQLAlchemy and Flask-Login requires:
1.  **OAuth Model**: A new model inheriting from `db.Model` and `OAuthConsumerMixin`. It requires a foreign key to the `User` model.
2.  **Blueprints**: Created using `make_google_blueprint` and `make_github_blueprint`.
3.  **SQLAlchemyBackend**: Attached to each blueprint, instructing Flask-Dance to use our database session and the `OAuth` model for token storage.
4.  **`oauth_authorized` Signal Hook**: This is fired after a successful OAuth dance. It is the hook where we fetch user information (like email) from the provider, check if a local user exists with that email (linking if yes, creating if no), and finally log the user in using `login_user()`.

## Missing Passwords & Passlib/Werkzeug
The `User` model in `app/models/user.py` currently requires a `password_hash` (`nullable=False`).
We need to handle the case where a user registers purely via OAuth and thus has no password.
- **Option 1**: Change `password_hash` to `nullable=True`. This is the cleanest approach.
- **Option 2**: Generate a random secure dummy password for OAuth-only users.
We will proceed with **Option 1** (`nullable=True`) as it explicitly represents "no password set", which makes it easy to hide/show the "Change Password" / "Set Password" forms.

## Dependencies
We need to add:
- `Flask-Dance[sqla]`
- `blinker` (Required by Flask-Dance for signals)

## Implementation Steps
1.  **Dependencies**: Add `Flask-Dance[sqla]` and `blinker` to `requirements.txt`.
2.  **Configuration**: Add `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GITHUB_OAUTH_CLIENT_ID`, `GITHUB_OAUTH_CLIENT_SECRET` to `config.py`.
3.  **Database**:
    - Modify `User` model `password_hash` column to `nullable=True`.
    - Create new `OAuth` model with `user_id` foreign key and `OAuthConsumerMixin`.
    - Generate migration and apply.
4.  **Blueprints Setup**:
    - Create `app/auth/oauth.py` to instantiate and configure the Google and GitHub blueprints with `SQLAlchemyBackend`.
    - Register these blueprints in `app/__init__.py`.
5.  **Signal Handling**:
    - Listen to `oauth_authorized` signal.
    - Fetch email from Google/GitHub API.
    - If email exists in DB, link account and login.
    - If not, create user, link account, and login.
6.  **Templates**:
    - Update `login.html` and `register.html` with Google and GitHub login buttons pointing to the respective Flask-Dance endpoints (`url_for('google.login')`, etc.).
    - Update `settings.html` to conditionally show "Set Password" instead of "Change Password" if `current_user.password_hash` is NULL.

## Missing Provider Emails
If an OAuth provider doesn't return an email (rare for Google, possible for GitHub depending on privacy settings), we need to handle it. Flask-Dance signals can return `False` to abort, and flash an error. In this phase, we'll flash an error asking them to provide an email or make it public, or we can prompt them in a separate view. Given the complexity of a multi-step registration flow, flashing an error and redirecting to the standard registration page is the simplest v1.

## Validation Architecture
- Verify `requirements.txt` contains `Flask-Dance[sqla]` and `blinker`.
- Verify database migration alters `password_hash` to be nullable and creates the `OAuth` table.
- Verify OAuth login routes exist and redirect to provider.
- Verify settings page logic (Set Password vs Change Password).
