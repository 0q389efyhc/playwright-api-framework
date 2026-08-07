import pytest

@pytest.mark.regression
def test_create_user_negative(api_client):
    response = api_client.post("/invalid-endpoint", {})

    assert response.status_code == 404