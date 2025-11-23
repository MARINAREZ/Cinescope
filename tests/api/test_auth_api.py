import pytest
import requests
from constants import AUTH_BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT, ADMIN_USER
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager
from api.auth_api import AuthApi

class TestPositiveAuthApi:
    # Регистрация нового пользователя
    def test_register_user(self, test_user):
        session = requests.Session()
        auth_api = AuthApi(session)

        response = auth_api.register_user(test_user=test_user)

        print(f'Response status: {response.status_code}')
        print(f'Response text: {response.json()}')
        assert response.status_code == 201, f'Ошибка регистрации пользователя'

        response_data = response.json()
        assert response_data['email'] == test_user['email'], f'Несоответствует email созданного пользователя'
        assert 'id' in response_data, 'ID пользователя отсутствует в ответе'
        assert 'roles' in response_data, 'roles пользователя отсутствует в ответе'
        assert 'USER' in response_data['roles'], 'USER пользователя отсутствует в ответе'

    # Авторизация нового пользователя
    def test_auth_user(self, test_user):
        session = requests.Session()
        auth_api = AuthApi(session)

        register_response = auth_api.register_user(test_user=test_user)
        assert register_response.status_code == 201, 'Ошибка регистрации'

        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        login_response = auth_api.login_user(test_user=login_data)
        assert login_response.status_code == 201, (f'Ошибка авторизации пользователя, получен /'
                                                          f'{login_response.status_code}')

        print(f'Response status: {login_response.status_code}')
        print(f'Response text: {login_response.json()}')

        response_data = login_response.json()
        assert response_data['user']['email'] == test_user['email'], 'Несоответствует email с данными'
        token = response_data.get('accessToken')
        assert token is not None, 'accessToken не найден'

class TestNegativeAuthApi:
    # Негативный сценарий авторизации пользователя(неверный password)
    def test_auth_user_error_password(self, test_user):
        session = requests.Session()
        auth_api = AuthApi(session)
        register_response = auth_api.register_user(test_user=test_user)

        negative_data= {
            "email": test_user["email"],
            "password": f"@{test_user['password']}"
        }

        negative_auth_response = auth_api.login_user(test_user=negative_data, expected_status=401)
        assert negative_auth_response.status_code == 401, \
            f"Ожидался статус 401, получен {negative_auth_response.status_code}"

        response_data = negative_auth_response.json()
        print(f'Тело ответа об ошибке:{response_data}')

    # Негативный сценарий авторизации пользователя(неверный email)
    def test_auth_user_error_email(self, test_user):
        session = requests.Session()
        auth_api = AuthApi(session)
        register_response = auth_api.register_user(test_user=test_user)

        negative_data = {
            "email": f'www{test_user["email"]}',
            "password": test_user["password"]
        }

        negative_auth = auth_api.login_user(test_user=negative_data, expected_status=401)
        assert negative_auth.status_code == 401, \
            f"Ожидался статус 401, получен {negative_auth.status_code}"

        response_data = negative_auth.json()
        print(f'Тело ответа об ошибке:{response_data}')