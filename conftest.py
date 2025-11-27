import pytest
from faker import Faker
from api.api_manager import ApiManager
from constants import ADMIN_USER

faker = Faker()

@pytest.fixture(scope='function')
def test_user():
    """Генерация случайного пользователя"""
    from utils.data_generator import DataGenerator
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
def movie_data():
    return {
        "name": faker.catch_phrase(),
        "imageUrl": faker.image_url(),
        "price": faker.random_int(min=100, max=1000),
        "description": faker.text(max_nb_chars=200),
        "location": faker.random_element(elements=("MSK", "SPB")),
        "published": True,
        "genreId": faker.random_int(min=1, max=10)
    }


@pytest.fixture(scope='function')
def update_movie_data():
    return {
        "name": faker.catch_phrase(),
        "imageUrl": faker.image_url(),
        "price": faker.random_int(min=100, max=1000),
        "description": faker.text(max_nb_chars=200),
        "location": faker.random_element(elements=("MSK", "SPB")),
        "published": True,
        "genreId": faker.random_int(min=1, max=10)
    }


@pytest.fixture(scope="function")
def admin_session():
    import requests
    session = requests.Session()
    api_manager = ApiManager(session)
    api_manager.auth_api.authenticate(ADMIN_USER)
    return api_manager

@pytest.fixture(scope='function')
def user_session(test_user):
    """ApiManager с авторизацией под обычным пользователем"""
    import requests
    session = requests.Session()
    api_manager = ApiManager(session)
    api_manager.auth_api.register_user(test_user=test_user)
    api_manager.auth_api.authenticate(test_user)
    return api_manager
