import json
import requests
import logging
import os

class CustomRequester:
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_requester(self, method, endpoint, json_data=None, params=None, expected_status=None, need_logging=True):
        url = f'{self.base_url}{endpoint}'
        response = self.session.request(method, url, json=json_data, params=params)

        if need_logging:
            self.log_request_and_response(response)

        # Проверяем статус только если он явно указан
        if expected_status is not None and response.status_code != expected_status:
            raise ValueError(f"Unexpected status code: {response.status_code}. Expected: {expected_status}")

        return response

    # Обновление заголовков сессии
    def update_headers(self, **kwargs):
        self.headers.update(kwargs)  # Обновляем базовые заголовки
        self.session.headers.update(self.headers)  # Обновляем заголовки в текущей сессии

    def log_request_and_response(self, response):
        try:
            print(f"REQUEST: {response.request.method} {response.request.url}")
            print(f"RESPONSE: {response.status_code} {response.text}")
        except AttributeError:
            print("Ошибка логирования: нет атрибута request")