import os

from flask import Flask, flash, redirect, render_template, request


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

    # Initialize extensions
    from app.extensions import db, login_manager, csrf, mail
    from flask_migrate import Migrate
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to continue.'
    login_manager.login_message_category = 'warning'
    login_manager.session_protection = 'basic'

    csrf.init_app(app)
    mail.init_app(app)

    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[app.config['RATELIMIT_DEFAULT']],
        storage_uri=app.config['RATELIMIT_STORAGE_URI'],
    )
    limiter.init_app(app)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        if user is None:
            return None
        if not user.is_active:
            return None
        return user

    # Register blueprints
    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.auth.oauth import init_oauth
    init_oauth(app)

    # Register error handlers (shared error template pattern per D-12)
    register_error_handlers(app)

    @app.errorhandler(429)
    def ratelimit_error(e):
        flash(f"Too many attempts. Please try again later.", 'warning')
        return redirect(request.url)

    # Register CLI commands
    from app.commands import register_commands
    register_commands(app)

    # Dev database bootstrap — create tables if missing
    if not app.config.get('TESTING') and app.config.get('DEBUG'):
        with app.app_context():
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            if not inspector.has_table('users'):
                db.create_all()

    return app


def register_error_handlers(app):
    """Register error handlers using a shared error.html template."""

    error_pages = {
        403: {
            'title': 'Access Forbidden',
            'message': "Sorry, you don't have permission to access this page.",
            'icon': 'bi-shield-lock'
        },
        404: {
            'title': 'Page Not Found',
            'message': "Oops! The page you're looking for doesn't exist.",
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
