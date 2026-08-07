from utils.faker_utils import get_user_data

def test_create_user(api_client):
    payload = get_user_data()

    response = api_client.post("/users", payload)

    assert response.status_code == 201