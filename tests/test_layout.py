def test_base_template_has_bootstrap(client):
    """LAYOUT-01: base.html includes Bootstrap 5.3 CDN CSS and JS bundle."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'bootstrap.min.css' in response.data
    assert b'bootstrap.bundle.min.js' in response.data


def test_viewport_meta(client):
    """MOB-03: base.html includes viewport meta tag for responsive layout."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'viewport' in response.data
    assert b'width=device-width' in response.data
