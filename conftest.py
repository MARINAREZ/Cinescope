# import requests
# from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
# import pytest
# from utils.data_generator import DataGenerator
#
# @pytest.fixture(scope="session")
# def test_user():
#     """
#     Генерация случайного пользователя для тестов.
#     """
#     random_email = DataGenerator.generate_random_email()
#     random_name = DataGenerator.generate_random_name()
#     random_password = DataGenerator.generate_random_password()
#
#     return {
#         "email": random_email,
#         "fullName": random_name,
#         "password": random_password,
#         "passwordRepeat": random_password,
#         "roles": ["USER"]
#     }
#
#
#     # Логинимся для получения токена
#     login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
#     login_data = {
#         "email": test_user["email"],
#         "password": test_user["password"]
#     }
#     response = requests.post(login_url, json=login_data, headers=HEADERS)
#     assert response.status_code == 200, "Ошибка авторизации"
#
#     # Получаем токен и создаём сессию
#     token = response.json().get("accessToken")
#     assert token is not None, "Токен доступа отсутствует в ответе"
#
#     session = requests.Session()
#     session.headers.update(HEADERS)
#     session.headers.update({"Authorization": f"Bearer {token}"})
#     return session


import pytest
import requests
from faker import Faker
from constants import REGISTER_ENDPOINT
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager

faker = Faker()

@pytest.fixture(scope="function")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="function")
def registered_user(test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="function")
def api_manager():
    """
    Фикстура для создания экземпляра ApiManager.
    """
    s = requests.Session()
    return ApiManager(session=s)

@pytest.fixture(scope="session")
def auth_session(test_user):
    # Регистрируем нового пользователя
    register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
    response = requests.post(register_url, json=test_user, headers=HEADERS)
    if response.status_code == 409:
        print("Пользователь уже существует, пробуем авторизоваться...")
    elif response.status_code == 201:
        print("Пользователь успешно зарегистрирован")
    else:
        assert False, f"Неожиданная ошибка регистрации: {response.status_code} - {response.text}"