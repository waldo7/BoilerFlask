def test_404_page(client):
    """LAYOUT-02: 404 response renders styled error page with 'Page Not Found'."""
    response = client.get('/nonexistent-page-12345')
    assert response.status_code == 404
    assert b'Page Not Found' in response.data
    assert b'Go Home' in response.data
