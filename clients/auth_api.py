import pytest
import requests
from constants import BASE_URL, HEADERS


class TestAuthAPI:
    def test_register_user(self, test_user):
        """
        Тест на регистрацию пользователя.
        """
        register_url = f"{BASE_URL}/register"
        response = requests.post(register_url, json=test_user, headers=HEADERS)

        assert response.status_code == 201, f"Ошибка регистрации: {response.text}"
        response_data = response.json()
        assert "id" in response_data
        assert response_data["email"] == test_user["email"]

    def test_register_and_login_user(self, test_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        # Регистрация
        register_url = f"{BASE_URL}/register"
        register_response = requests.post(register_url, json=test_user, headers=HEADERS)
        assert register_response.status_code == 201, f"Ошибка регистрации: {register_response.text}"

        # Авторизация
        login_url = f"{BASE_URL}/login"
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        login_response = requests.post(login_url, json=login_data, headers=HEADERS)
        assert login_response.status_code == 200, f"Ошибка авторизации: {login_response.text}"

        login_data = login_response.json()
        assert "accessToken" in login_data
        assert login_data["user"]["email"] == test_user["email"]