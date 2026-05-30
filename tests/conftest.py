import pytest
from app import create_app


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
    })
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()
