from flask import current_app, flash, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_login import current_user, login_user

from app.extensions import db
from app.models.user import OAuth, User

google_blueprint = None
github_blueprint = None


def init_oauth(app):
    global google_blueprint, github_blueprint

    google_blueprint = make_google_blueprint(
        client_id=app.config.get('GOOGLE_OAUTH_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_OAUTH_CLIENT_SECRET'),
        scope=['profile', 'email'],
        storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
    )

    github_blueprint = make_github_blueprint(
        client_id=app.config.get('GITHUB_OAUTH_CLIENT_ID'),
        client_secret=app.config.get('GITHUB_OAUTH_CLIENT_SECRET'),
        scope=['user:email'],
        storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
    )

    _register_signals()

    app.register_blueprint(google_blueprint, url_prefix='/login')
    app.register_blueprint(github_blueprint, url_prefix='/login')


def _register_signals():
    @oauth_authorized.connect_via(google_blueprint)
    def google_logged_in(blueprint, token):
        if not token:
            flash('Access denied — Google login failed.', 'danger')
            return False

        resp = blueprint.session.get('/oauth2/v2/userinfo')
        if not resp.ok:
            flash('Failed to fetch your email from Google.', 'danger')
            return False

        info = resp.json()
        email = info.get('email')
        if not email:
            flash(
                'Google did not provide an email address. '
                'Please ensure your Google account has a verified email.',
                'danger',
            )
            return False

        email = email.strip().lower()
        return _handle_oauth_login(email)

    @oauth_authorized.connect_via(github_blueprint)
    def github_logged_in(blueprint, token):
        if not token:
            flash('Access denied — GitHub login failed.', 'danger')
            return False

        resp = blueprint.session.get('/user/emails')
        if not resp.ok:
            flash('Failed to fetch your email from GitHub.', 'danger')
            return False

        emails = resp.json()
        primary = next(
            (e['email'] for e in emails if e.get('primary') and e.get('verified')),
            None,
        )
        if not primary:
            flash(
                'GitHub did not provide a verified primary email. '
                'Please add a verified email to your GitHub account and set it public.',
                'danger',
            )
            return False

        primary = primary.strip().lower()
        return _handle_oauth_login(primary)


def _handle_oauth_login(email):
    if current_user.is_authenticated:
        flash(f'Your account is now linked with {email}.', 'success')
        return False

    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email=email, role='USER')
        db.session.add(user)
        db.session.commit()

    login_user(user)
    flash('Welcome! You have been signed in.', 'success')
    return redirect(url_for('main.dashboard'))
