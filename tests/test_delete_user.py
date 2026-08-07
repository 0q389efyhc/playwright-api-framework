import pytest

@pytest.mark.regression
def test_delete_user(api_client):
    response = api_client.delete("/users/1")

    assert response.status_code in [200, 204]