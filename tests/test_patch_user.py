import pytest

@pytest.mark.regression
def test_patch_user(api_client):
    payload = {
        "job": "Automation Engineer"
    }

    response = api_client.patch("/users/1", payload)

    assert response.status_code in [200, 201]