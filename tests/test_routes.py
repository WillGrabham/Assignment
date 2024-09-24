def test_200_login(test_client):
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_404_page(test_client):
    response = test_client.get("/a/made/up/url")
    assert response.status_code == 404
    assert b"Page not found, go home?" in response.data


def test_redirect_to_login_when_logged_out(test_client):
    response = test_client.get("/")
    assert response.status_code == 302
    redirect_response = test_client.get("/", follow_redirects=True)
    assert b"Login" in redirect_response.data
