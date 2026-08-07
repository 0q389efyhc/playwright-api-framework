import pytest

@pytest.mark.smoke
def test_create_user(api_client):
    payload = {
        "name": "Pranjal",
        "job": "QA"
    }

    response = api_client.post("/users", payload)

    assert response.status_code in [200, 201]