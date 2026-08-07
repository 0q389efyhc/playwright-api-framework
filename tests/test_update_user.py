def test_update_user(api_client):
    payload = {
        "name": "Dennis",
        "email": "dennis@test.com"
    }

    response = api_client.put("/users/1", payload)

    assert response.status_code in [200, 201]