import pytest

@pytest.mark.regression
def test_update_user(api_client):
    payload = {
        "name": "Updated User"
    }

    response = api_client.put("/users/1", payload)

    assert response.status_code in [200, 201]