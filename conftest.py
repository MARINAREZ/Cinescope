import pytest
import requests
from faker import Faker
from utils.data_generator import DataGenerator
from clients.movies_manager import MoviesManager
from clients.api_manager import ApiManager
from constants import *

faker = Faker()


@pytest.fixture(scope="function")
def admin_session():
    """
    Фикстура для аутентифицированной сессии администратора.
    """
    # Креды администратора
    admin_credentials = {
        "email": "api1@gmail.com",
        "password": "asdqwe123Q"
    }

    # Логинимся для получения токена
    login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    login_response = requests.post(login_url, json=admin_credentials, headers=HEADERS)
    assert login_response.status_code == 200, f"Ошибка авторизации администратора: {login_response.text}"

    # Получаем токен
    token_data = login_response.json()
    access_token = token_data["accessToken"]
    assert access_token is not None, "Токен доступа отсутствует"

    # Создаем сессию с токеном
    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {access_token}"})

    return session


@pytest.fixture(scope="function")
def movies_manager(admin_session):
    """
    Фикстура для менеджера фильмов.
    """
    return MoviesManager(admin_session)


@pytest.fixture(scope="function")
def create_movie_data():
    """
    Фикстура с данными для создания фильма.
    Согласно ошибке API ожидает поля: name, price, description, location, published, genreId
    """
    return {
        "name": f"Тестовый фильм {faker.word()} {faker.random_int(1, 1000)}",
        "description": faker.text(max_nb_chars=200),
        "price": faker.random_int(100, 1000),
        "location": faker.random_element(["MSK", "SPB"]),
        "published": faker.boolean(),
        "genreId": faker.random_int(1, 10)
    }


@pytest.fixture(scope="function")
def created_movie(movies_manager, create_movie_data):
    """
    Фикстура создает фильм и возвращает его данные.
    Удаляет фильм после теста.
    """
    response = movies_manager.create_movie(create_movie_data)
    movie_data = response.json()

    yield movie_data

    try:
        movies_manager.delete_movie(movie_data["id"])
    except:
        pass


# Добавляем старые фикстуры для auth тестов
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