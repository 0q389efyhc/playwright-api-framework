def test_patch_user(api_client):
    payload = {"name": "Updated User"}

    response = api_client.patch("/users/1", payload)

    assert response.status_code in [200, 201]