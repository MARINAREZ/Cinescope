# clients/api_manager.py
import requests


class ApiManager:
    def __init__(self, session=None):
        self.session = session or requests.Session()

    def _send_request(self, method, endpoint, data=None, params=None, expected_status=200):
        """Базовый метод для отправки запросов"""
        url = f"{self.base_url}{endpoint}"

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params
        )

        if expected_status is not None and response.status_code != expected_status:
            raise AssertionError(
                f"Expected status {expected_status}, but got {response.status_code}. "
                f"Response: {response.text}"
            )

        return response

    def send_request(self, method, endpoint, data=None, params=None, expected_status=200):
        """Публичный метод для отправки запросов"""
        return self._send_request(method, endpoint, data, params, expected_status)