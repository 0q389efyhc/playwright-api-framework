import pytest

@pytest.mark.regression
def test_invalid_user(api_client):
    response = api_client.get("/users/99999")

    assert response.status_code in [404]