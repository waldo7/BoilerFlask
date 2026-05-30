import pytest

from app import create_app


@pytest.fixture
def app():
    """Create and configure a Flask app for testing with in-memory database."""
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
    })

    with app.app_context():
        from app.extensions import db
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()


@pytest.fixture
def _db(app):
    """Create all database tables for a test and drop them after."""
    from app.extensions import db
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture
def user(_db):
    """Create a test User with role=USER in the database."""
    from app.extensions import db
    from app.models.user import Role, User
    user = User(email='test@example.com', role=Role.USER)
    user.set_password('Test1234!')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def admin_user(_db):
    """Create an admin User with role=ADMIN in the database."""
    from app.extensions import db
    from app.models.user import Role, User
    user = User(email='admin@example.com', role=Role.ADMIN)
    user.set_password('Admin1234!')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def auth_client(client, user):
    """Test client with authenticated user session."""
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'Test1234!',
        'remember': False,
    }, follow_redirects=True)
    return client
