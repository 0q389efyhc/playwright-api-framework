import requests
from utils.logger import logger


class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        logger.info(f"GET Request: {self.base_url}{endpoint}")
        response = requests.get(f"{self.base_url}{endpoint}")
        logger.info(f"Response: {response.status_code}")
        return response

    def post(self, endpoint, payload):
        logger.info(f"POST Request: {self.base_url}{endpoint}")
        logger.info(f"Payload: {payload}")
        response = requests.post(
            f"{self.base_url}{endpoint}",
            json=payload
        )
        logger.info(f"Response: {response.status_code}")
        return response

    def put(self, endpoint, payload):
        logger.info(f"PUT Request: {self.base_url}{endpoint}")
        response = requests.put(
            f"{self.base_url}{endpoint}",
            json=payload
        )
        logger.info(f"Response: {response.status_code}")
        return response

    def patch(self, endpoint, payload):
        logger.info(f"PATCH Request: {self.base_url}{endpoint}")
        response = requests.patch(
            f"{self.base_url}{endpoint}",
            json=payload
        )
        logger.info(f"Response: {response.status_code}")
        return response

    def delete(self, endpoint):
        logger.info(f"DELETE Request: {self.base_url}{endpoint}")
        response = requests.delete(
            f"{self.base_url}{endpoint}"
        )
        logger.info(f"Response: {response.status_code}")
        return response