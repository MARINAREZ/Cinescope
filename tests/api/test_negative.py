import requests
from constants import *

class TestAuthAPI:
    def test_register_user(self, test_user):
        # URL для регистрации
        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"

        # Отправка запроса на регистрацию
        response = requests.post(register_url, json=test_user, headers=HEADERS)

        # Логируем ответ для диагностики
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        # Проверки
        assert response.status_code == 201, "Ошибка регистрации пользователя"
        response_data = response.json()
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"

        # Проверяем, что роль USER назначена по умолчанию
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

class TestNegativeAuthAPI:
    def test_error_password(self, test_user):
        """Тест авторизации с неправильным паролем"""
        # Данные с неправильным паролем
        login_error_data = {
            "email": test_user["email"],
            "password": "error"
        }

        # Вызывание метода для отображения ошибки
        response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=login_error_data, headers=HEADERS)
        assert response.status_code in [400, 401, 500], "Должны получить 400, 401 или 500 статус-код"

    def test_error_email(self, test_user):
        """Тест авторизации с неправильным логином"""
        # Данные с неправильным логином
        login_error_data = {
            "email": "nonexistent@example.com",
            "password": test_user["password"]
        }

        # Вызывание метода для отображения ошибки
        response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=login_error_data, headers=HEADERS)
        assert response.status_code in [400, 401, 404], f"Ожидался статус 400, 401 или 404, получен {response.status_code}"

    def test_empty_credentials(self):
        """Тест авторизации с пустыми данными"""
        login_error_data = {
            "email": "",
            "password": ""
        }

        response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=login_error_data, headers=HEADERS)
        print(f"Empty credentials response: {response.status_code} - {response.text}")
        assert response.status_code in [400, 401], "Ожидалась ошибка валидации"
