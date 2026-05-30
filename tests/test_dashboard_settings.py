def test_dashboard_access(auth_client):
    """MAIN-02: Dashboard is accessible to logged in users and passes context."""
    response = auth_client.get('/dashboard')
    assert response.status_code == 200
    assert b'Account Profile' in response.data


def test_settings_access(auth_client):
    """MAIN-03: Settings route is accessible."""
    response = auth_client.get('/settings')
    assert response.status_code == 200
    assert b'Account Settings' in response.data
    assert b'Change Password' in response.data


def test_dashboard_admin_gating(client, admin_user):
    """AUTH-06: Dashboard shows Admin elements to ADMIN roles."""
    client.post('/auth/login', data={'email': admin_user.email, 'password': 'Admin1234!', 'remember': False})
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Total Users' in response.data
    assert b'System Config' in response.data
    assert b'System Admin' in response.data


def test_sidebar_admin_tools(client, admin_user):
    """MAIN-03: Sidebar shows Admin Tools to ADMIN."""
    client.post('/auth/login', data={'email': admin_user.email, 'password': 'Admin1234!', 'remember': False})
    response = client.get('/dashboard')
    assert b'Admin Tools' in response.data
    assert b'System Settings' in response.data


def test_settings_change_password(auth_client):
    """AUTH-06: Password change logic verifies current and redirects."""
    # Invalid current password
    response = auth_client.post('/settings', data={
        'current_password': 'WrongPassword123!',
        'new_password': 'NewPassword1234!',
        'confirm_password': 'NewPassword1234!'
    }, follow_redirects=True)
    assert b'Incorrect current password.' in response.data

    # Valid current password
    response = auth_client.post('/settings', data={
        'current_password': 'Test1234!',
        'new_password': 'NewPassword1234!',
        'confirm_password': 'NewPassword1234!'
    }, follow_redirects=True)
    assert b'Your password has been changed successfully' in response.data
    assert b'Log In' in response.data
