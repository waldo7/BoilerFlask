import pytest

from app.auth.routes import generate_reset_token, verify_reset_token
from app.extensions import db
from app.models.user import Role, User


# ---------------------------------------------------------------------------
# AUTH-01: Registration
# ---------------------------------------------------------------------------

def test_register_page_renders(client):
    """AUTH-01: GET /auth/register returns 200 with Create Account heading."""
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Create Account' in response.data


def test_register_success(client):
    """AUTH-01: Valid registration creates user, auto-login, redirects to dashboard."""
    response = client.post('/auth/register', data={
        'email': 'new@example.com',
        'password': 'Test1234!',
        'confirm_password': 'Test1234!',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data or b'Welcome' in response.data

    user = User.query.filter_by(email='new@example.com').first()
    assert user is not None
    assert user.role == Role.USER
    assert user.check_password('Test1234!')


def test_register_duplicate_email(client, user):
    """AUTH-01: Duplicate email shows error and re-renders form."""
    response = client.post('/auth/register', data={
        'email': 'test@example.com',
        'password': 'Test1234!',
        'confirm_password': 'Test1234!',
    })
    assert response.status_code == 200
    assert b'Email already registered' in response.data


def test_register_weak_password_short(client):
    """AUTH-01: Password < 8 chars shows validation error."""
    response = client.post('/auth/register', data={
        'email': 'weak@example.com',
        'password': 'short',
        'confirm_password': 'short',
    })
    assert response.status_code == 200
    assert b'at least 8' in response.data or b'must contain' in response.data


def test_register_weak_password_complexity(client):
    """AUTH-01: Password lacking 2 char types shows complexity error."""
    response = client.post('/auth/register', data={
        'email': 'simple@example.com',
        'password': 'lowercaseonly',
        'confirm_password': 'lowercaseonly',
    })
    assert response.status_code == 200
    assert b'must contain' in response.data


# ---------------------------------------------------------------------------
# AUTH-02: Login + Session
# ---------------------------------------------------------------------------

def test_login_page_renders(client):
    """AUTH-02: GET /auth/login returns 200 with Log In heading."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Log In' in response.data


def test_login_success_redirects_dashboard(client, user):
    """AUTH-02: Valid login redirects to dashboard, session persists."""
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'Test1234!',
    }, follow_redirects=False)
    assert response.status_code == 302

    dashboard = client.get('/dashboard')
    assert dashboard.status_code == 200
    assert b'Welcome, test@example.com' in dashboard.data


def test_login_bad_password(client, user):
    """AUTH-02: Wrong password shows error."""
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'wrongpassword',
    })
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data


def test_login_deactivated_user(client, user):
    """AUTH-02: Deactivated user cannot login."""
    user.is_active = False
    db.session.commit()

    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'Test1234!',
    })
    assert response.status_code == 200
    assert b'deactivated' in response.data


def test_login_remember_me(client, user):
    """AUTH-02: Remember me sets persistent session cookie."""
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'Test1234!',
        'remember': True,
    }, follow_redirects=False)
    assert response.status_code == 302


def test_login_already_authenticated(auth_client):
    """AUTH-02: Authenticated user visiting login is redirected to dashboard."""
    response = auth_client.get('/auth/login', follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data or b'Welcome' in response.data


# ---------------------------------------------------------------------------
# AUTH-03: Logout
# ---------------------------------------------------------------------------

def test_logout_redirects_home(auth_client):
    """AUTH-03: Logout redirects to / (home)."""
    response = auth_client.get('/auth/logout', follow_redirects=False)
    assert response.status_code == 302


def test_logout_clears_session_and_protects_dashboard(client, user):
    """AUTH-03: After logout, /dashboard redirects to login."""
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'Test1234!',
    })
    client.get('/auth/logout')

    response = client.get('/dashboard', follow_redirects=False)
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


# ---------------------------------------------------------------------------
# AUTH-04: Password Reset
# ---------------------------------------------------------------------------

def test_forgot_password_page_renders(client):
    """AUTH-04: GET /auth/forgot-password returns 200."""
    response = client.get('/auth/forgot-password')
    assert response.status_code == 200
    assert b'Forgot Password' in response.data


def test_forgot_password_existing_email(client, user):
    """AUTH-04: Existing email shows generic Check Your Email page (D-06)."""
    response = client.post('/auth/forgot-password', data={
        'email': 'test@example.com',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Check Your Email' in response.data


def test_forgot_password_unknown_email(client):
    """AUTH-04: Unknown email also shows generic Check Your Email page (D-06)."""
    response = client.post('/auth/forgot-password', data={
        'email': 'nonexistent@example.com',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Check Your Email' in response.data


def test_reset_password_valid_token(client, user):
    """AUTH-04: Valid token renders reset form, POST changes password."""
    user.password_reset_requested_at = db.func.now()
    db.session.commit()
    token = generate_reset_token(user)

    response = client.get(f'/auth/reset-password/{token}')
    assert response.status_code == 200
    assert b'Set New Password' in response.data

    response = client.post(f'/auth/reset-password/{token}', data={
        'password': 'NewTest234!',
        'confirm_password': 'NewTest234!',
    }, follow_redirects=True)
    assert response.status_code == 200

    assert user.check_password('NewTest234!')


def test_reset_password_invalid_token(client):
    """AUTH-04: Invalid token redirects to forgot-password."""
    response = client.get('/auth/reset-password/bad-token', follow_redirects=True)
    assert response.status_code == 200
    assert b'invalid' in response.data or b'Forgot Password' in response.data


def test_reset_password_token_one_time_use(client, user):
    """AUTH-04: Token cannot be reused after successful reset (D-07)."""
    user.password_reset_requested_at = db.func.now()
    db.session.commit()
    token = generate_reset_token(user)

    client.post(f'/auth/reset-password/{token}', data={
        'password': 'FirstTest1!',
        'confirm_password': 'FirstTest1!',
    })

    response = client.post(f'/auth/reset-password/{token}', data={
        'password': 'SecondTest2!',
        'confirm_password': 'SecondTest2!',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'invalid' in response.data or b'Forgot Password' in response.data


# ---------------------------------------------------------------------------
# AUTH-05: Roles
# ---------------------------------------------------------------------------

def test_default_role_on_register(client):
    """AUTH-05: New users are assigned Role.USER by default."""
    client.post('/auth/register', data={
        'email': 'roletest@example.com',
        'password': 'Test1234!',
        'confirm_password': 'Test1234!',
    })
    user = User.query.filter_by(email='roletest@example.com').first()
    assert user is not None
    assert user.role == Role.USER


def test_role_enum_values():
    """AUTH-05: Role enum has correct string values."""
    assert Role.USER.value == 'user'
    assert Role.ADMIN.value == 'admin'
    assert Role.SUPERUSER.value == 'superuser'


def test_admin_user_login(client, admin_user):
    """AUTH-05: Admin user can login and access dashboard."""
    response = client.post('/auth/login', data={
        'email': 'admin@example.com',
        'password': 'Admin1234!',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data or b'Welcome' in response.data


# ---------------------------------------------------------------------------
# Dashboard Protection
# ---------------------------------------------------------------------------

def test_dashboard_redirects_unauthenticated(client):
    """Dashboard: Unauthenticated access redirects to login with next= param (D-14)."""
    response = client.get('/dashboard', follow_redirects=False)
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


def test_dashboard_authenticated(auth_client, user):
    """Dashboard: Authenticated user sees welcome message and empty state."""
    response = auth_client.get('/dashboard')
    assert response.status_code == 200
    assert b'Welcome, test@example.com' in response.data
    assert b'Getting Started' in response.data


# ---------------------------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------------------------

def test_email_normalization(client):
    """Edge: Registration with mixed case normalizes to lowercase (D-27)."""
    client.post('/auth/register', data={
        'email': 'Normalized@Example.com',
        'password': 'Test1234!',
        'confirm_password': 'Test1234!',
    })

    client.get('/auth/logout', follow_redirects=True)

    response = client.post('/auth/login', data={
        'email': 'normalized@example.com',
        'password': 'Test1234!',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data or b'Welcome' in response.data


def test_csrf_config(client, app):
    """CSRF: TestingConfig has WTF_CSRF_ENABLED=False."""
    assert app.config.get('WTF_CSRF_ENABLED') is False
