import pytest
from api.api_client import APIClient
from config.config import BASE_URL


@pytest.fixture
def api_client():
    return APIClient(BASE_URL)