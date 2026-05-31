def test_homepage(client):
    """MAIN-01: Homepage returns 200 with 'BoilerFlask' brand text."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'BoilerFlask' in response.data
