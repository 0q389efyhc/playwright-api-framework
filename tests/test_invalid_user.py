def test_invalid_user(api_client):
    response = api_client.get("/users/9999")
    assert response.status_code == 404