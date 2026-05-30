def test_homepage(client):
    """MAIN-01: Homepage returns 200 with 'Flask app is running' placeholder."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Flask app is running' in response.data
