import requests
import pytest
from constants import *
from api.movies_api import MoviesApi
from custom_requester.custom_requester import CustomRequester
from api.auth_api import AuthApi
from utils.data_generator import DataGenerator
from faker import Faker
from api.api_manager import ApiManager

faker = Faker()

@pytest.fixture
def api_manager(requester):
    return ApiManager(requester.session)

@pytest.fixture(scope="function")
def auth_api():
    session = requests.Session()
    return AuthApi(session)

@pytest.fixture(scope='function')
def test_user():
    # Генерация случайного пользователя для тестов
    random_email = DataGenerator.generate_random_mail()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope='function')
def register_auth_user(requester, test_user):
    response = requester.send_requester(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        json_data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture
def movie_data():
    return {
        "name": faker.catch_phrase(),
        "imageUrl": faker.image_url(),
        "price": faker.random_int(min=100, max=1000),
        "description": faker.text(max_nb_chars=200),
        "location": faker.city(),
        "published": True,
        "genreId": faker.random_int(min=1, max=10)
    }

@pytest.fixture
def update_movie_data():
    return {
        "name": faker.catch_phrase(),
        "imageUrl": faker.image_url(),
        "price": faker.random_int(min=100, max=1000),
        "description": faker.text(max_nb_chars=200),
        "location": faker.city(),
        "published": True,
        "genreId": faker.random_int(min=1, max=10)
    }

@pytest.fixture(scope="function")
def session():
    # Фикстура для MoviesApi
    session_obj = requests.Session()
    return MoviesApi(session=session_obj)