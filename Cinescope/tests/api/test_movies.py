import pytest
import requests
from constants import MOVIE_BASE_URL
from api.movies_api import MoviesApi
from api.auth_api import AuthApi


class TestPositiveMoves:
    # Тест на получение списка фильмов
    def test_get_movies(self, session):
        get_movies = session.get_movies()

        movies_response = get_movies.json()
        assert isinstance(movies_response, dict), 'Ответ должен быть словарем'
        assert 'movies' in movies_response, 'Ключ movies отсутствует в ответе'
        assert isinstance(movies_response['movies'], list), 'movies должен быть списком'

        movies_list = movies_response['movies']
        print(f"Получено фильмов: {len(movies_list)}")

    # Тест на получение фильма по ID
    def test_get_movies_by_id(self, session):
        # Используем существующий ID фильма
        existing_movie_id = 1

        get_movies_by_id = session.get_movies_by_id(movie_id=existing_movie_id)

        movie = get_movies_by_id.json()
        assert movie is not None, f'Фильм не найден'
        assert 'id' in movie, 'ID фильма отсутствует в ответе'
        assert movie['id'] == existing_movie_id, 'ID фильма не соответствует запрошенному'


class TestNegativeMoves:
    # Тест, что пользователь USER не может создавать фильмы
    def test_create_movie_forbidden(self, session, movie_data, test_user):
        auth_session = requests.Session()
        auth_api = AuthApi(auth_session)

        # Регистрируем и логиним пользователя
        auth_api.register_user(test_user=test_user)
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        login_response = auth_api.login_user(test_user=login_data, expected_status=201)
        token = login_response.json()["accessToken"]

        # Устанавливаем токен в сессию
        session.update_headers(authorization=f"Bearer {token}")

        # Пытаемся создать фильм - ожидаем 403
        create_response = session.create_movies(movie_data=movie_data,
                                                expected_status=403)
        assert create_response.status_code == 403, "USER не должен иметь права создавать фильмы"

    # Тест, что пользователь USER не может изменять фильмы
    def test_patch_movie_forbidden(self, session, update_movie_data, test_user):
        auth_session = requests.Session()
        auth_api = AuthApi(auth_session)

        # Регистрируем и логиним пользователя
        auth_api.register_user(test_user=test_user)
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        login_response = auth_api.login_user(test_user=login_data, expected_status=201)
        token = login_response.json()["accessToken"]

        # Устанавливаем токен в сессию
        session.update_headers(authorization=f"Bearer {token}")

        # Пытаемся изменить существующий фильм
        existing_movie_id = 1
        patch_response = session.patch_movies_by_id(
            movie_id=existing_movie_id,
            update_movie_data=update_movie_data,
            expected_status=403
        )
        assert patch_response.status_code == 403, "USER не должен иметь права изменять фильмы"

    # Тест, что пользователь USER не может удалять фильмы
    def test_delete_movie_forbidden(self, session, test_user):
        auth_session = requests.Session()
        auth_api = AuthApi(auth_session)

        # Регистрируем и логиним пользователя
        auth_api.register_user(test_user=test_user)
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        login_response = auth_api.login_user(test_user=login_data, expected_status=201)
        token = login_response.json()["accessToken"]

        # Устанавливаем токен в сессию
        session.update_headers(authorization=f"Bearer {token}")

        # Пытаемся удалить существующий фильм - ожидаем 403
        existing_movie_id = 1
        delete_response = session.delete_movies_by_id(
            movie_id=existing_movie_id,
            expected_status=403
        )
        assert delete_response.status_code == 403, "USER не должен иметь права удалять фильмы"