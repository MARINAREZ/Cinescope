import pytest
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT


class TestAuthAPI:
    def test_register_user(self):
        """Негативный тест регистрации с невалидными данными"""
        invalid_user = {
            "email": "invalid-email",
            "fullName": "Test User",
            "password": "short",
            "passwordRepeat": "short",
            "roles": ["USER"]
        }

        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
        response = requests.post(register_url, json=invalid_user, headers=HEADERS)

        # Ожидаем ошибку валидации
        assert response.status_code == 400, f"Ожидалась ошибка валидации, но получили {response.status_code}"


class TestNegativeAuthAPI:
    def test_error_password(self, test_user):
        """Тест на ошибку при неверном пароле"""
        # Сначала регистрируем пользователя
        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
        register_response = requests.post(register_url, json=test_user, headers=HEADERS)
        assert register_response.status_code == 201, "Ошибка регистрации пользователя"

        # Пытаемся войти с неверным паролем
        login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
        wrong_password_data = {
            "email": test_user["email"],
            "password": "WrongPassword123"  # Неверный пароль
        }
        login_response = requests.post(login_url, json=wrong_password_data, headers=HEADERS)

        # Ожидаем ошибку авторизации (401 Unauthorized)
        assert login_response.status_code == 401, "Ожидалась ошибка авторизации"
        response_data = login_response.json()
        assert "error" in response_data or "message" in response_data

    def test_error_email(self, test_user):
        """Тест на ошибку при неверном email"""
        # Регистрируем пользователя
        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
        register_response = requests.post(register_url, json=test_user, headers=HEADERS)
        assert register_response.status_code == 201, "Ошибка регистрации пользователя"

        # Пытаемся войти с неверным email
        login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
        wrong_email_data = {
            "email": "wrong@example.com",  # Неверный email
            "password": test_user["password"]
        }
        login_response = requests.post(login_url, json=wrong_email_data, headers=HEADERS)

        # Ожидаем ошибку авторизации (401 Unauthorized)
        assert login_response.status_code == 401, "Ожидалась ошибка авторизации"
        response_data = login_response.json()
        assert "error" in response_data or "message" in response_data

    def test_empty_credentials(self):
        """Тест на ошибку при пустых учетных данных"""
        login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
        empty_data = {
            "email": "",
            "password": ""
        }
        login_response = requests.post(login_url, json=empty_data, headers=HEADERS)

        # Ожидаем ошибку валидации (401 Unauthorized для этого API)
        assert login_response.status_code == 401, "Ожидалась ошибка авторизации"
        response_data = login_response.json()
        assert "error" in response_data or "message" in response_data