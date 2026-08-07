import pytest

@pytest.mark.smoke
def test_get_user(api_client):
    response = api_client.get("/users/1")

    assert response.status_code == 200