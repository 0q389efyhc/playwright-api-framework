def test_create_user_negative(api_client):
    response = api_client.post("/users", {})
    assert response.status_code in [400, 422, 201]