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
