import pytest
import requests
from custom_requester.custom_requester import CustomRequester
from constants import AUTH_BASE_URL, REGISTER_ENDPOINT, LOGOUT_ENDPOINT, LOGIN_ENDPOINT, ADMIN_USER

class AuthApi(CustomRequester):
    """Класс для работы с аутентификацией"""
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    # Регистрация нового пользователя
    def register_user(self, test_user, expected_status=201):
        return self.send_requester(
            method="POST",
            endpoint= REGISTER_ENDPOINT,
            json_data = test_user,
            expected_status = expected_status
        )

    # Авторизация пользователя
    def login_user(self, test_user, expected_status=201):
        return self.send_requester(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            json_data=test_user,
            expected_status=expected_status
        )

    # Выход из авторизации пользователя
    def logout(self, expected_status=200):
        return self.send_requester(
            method="GET",
            endpoint = LOGOUT_ENDPOINT,
            expected_status = expected_status
        )

    # Аутентификация
    def authenticate(self, user_creds):
        login_data = {
            "email": user_creds["email"],
            "password": user_creds["password"]
        }
        response = self.login_user(login_data)
        response_json = response.json()
        if "accessToken" not in response_json:
            raise KeyError("token is missing")
        token = response_json["accessToken"]
        self.update_headers(authorization=f"Bearer {token}")

