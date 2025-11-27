import pytest
import requests
from constants import MOVIE_BASE_URL, ADMIN_USER
from api.movies_api import MoviesApi
from api.auth_api import AuthApi

import pytest
from constants import ADMIN_USER


class TestPositiveMovies:
    # Тест на получение списка фильмов с фильтром location
    def test_get_movies_filtered(self, admin_session):
        params = {"location": "MSK"}
        resp = admin_session.movies_api.get_movies(params=params)
        movies_response = resp.json()

        print(f'Response: {movies_response}')
        assert isinstance(movies_response, dict), 'Ответ должен быть словарем'
        assert 'movies' in movies_response, 'Ключ movies отсутствует в ответе'
        assert isinstance(movies_response['movies'], list), 'movies должен быть списком'

        movies_list = [m for m in movies_response['movies'] if m["location"] == "MSK"]
        for movie in movies_list:
            assert movie["location"] == "MSK"

    # Тест на получение фильма по ID
    def test_get_movies_by_id_existing(self, admin_session, movie_data):
        # Создаём фильм
        create_resp = admin_session.movies_api.create_movies(movie_data)
        movie_id = create_resp.json()["id"]

        resp = admin_session.movies_api.get_movies_by_id(movie_id=movie_id)
        movie_response = resp.json()

        print(f'GET movie response: {movie_response}')
        assert movie_response['id'] == movie_id, 'ID фильма не соответствует'
        assert movie_response['name'] == movie_data['name'], 'Имя фильма не соответствует'

        # Удаляем фильм
        resp_delete = admin_session.movies_api.delete_movies_by_id(movie_id=movie_id)
        assert resp_delete.status_code == 200

    # Позитивный тест: фильм не существует
    def test_get_movies_by_id_not_existing(self, admin_session):
        resp = admin_session.movies_api.get_movies_by_id(movie_id=999999, expected_status=404)
        print(f'GET non-existing movie response: {resp.json()}')
        assert resp.status_code == 404

    # Тест на создание фильма
    def test_post_movies(self, admin_session, movie_data):
        resp = admin_session.movies_api.create_movies(movie_data=movie_data)
        movie_response = resp.json()

        print(f'POST movie response: {movie_response}')
        assert 'id' in movie_response
        for key in ['name', 'price', 'location', 'genreId', 'published']:
            assert movie_response[key] == movie_data[key]

        # Удаляем созданный фильм
        resp_delete = admin_session.movies_api.delete_movies_by_id(movie_id=movie_response['id'])
        assert resp_delete.status_code == 200

    # Тест на изменение фильма
    def test_patch_movies_by_id(self, admin_session, update_movie_data, movie_data):
        # Создаём фильм
        create_resp = admin_session.movies_api.create_movies(movie_data)
        movie_id = create_resp.json()["id"]

        # PATCH фильма
        patch_resp = admin_session.movies_api.patch_movies_by_id(
            movie_id=movie_id,
            update_movie_data=update_movie_data
        )
        updated_movie = patch_resp.json()
        print(f'PATCH movie response: {updated_movie}')
        for key in update_movie_data:
            assert updated_movie[key] == update_movie_data[key]

        # Удаляем фильм
        resp_delete = admin_session.movies_api.delete_movies_by_id(movie_id=movie_id)
        assert resp_delete.status_code == 200

    # Тест на удаление фильма
    def test_delete_movies(self, admin_session, movie_data):
        # Создаём фильм
        create_resp = admin_session.movies_api.create_movies(movie_data)
        movie_id = create_resp.json()['id']

        # Удаляем фильм
        resp_delete = admin_session.movies_api.delete_movies_by_id(movie_id=movie_id)
        print(f'DELETE movie response: {resp_delete.status_code}')
        assert resp_delete.status_code == 200

    # Негативный тест: создание фильма с невалидными данными
    def test_create_movie_invalid_data(self, admin_session):
        invalid_data = {"name": "", "price": "invalid"}
        resp = admin_session.movies_api.create_movies(invalid_data, expected_status=400)
        print(f'Invalid POST response: {resp.json()}')
        assert resp.status_code == 400


class TestNegativeMovies:

    # USER не может создавать фильмы
    def test_create_movie_forbidden(self, user_session, movie_data):
        resp = user_session.movies_api.create_movies(movie_data, expected_status=403)
        print(f'Forbidden POST response: {resp.status_code}')
        assert resp.status_code == 403

    # USER не может изменять фильмы
    def test_patch_movie_forbidden(self, user_session, update_movie_data):
        resp = user_session.movies_api.patch_movies_by_id(
            movie_id=1,
            update_movie_data=update_movie_data,
            expected_status=403
        )
        print(f'Forbidden PATCH response: {resp.status_code}')
        assert resp.status_code == 403

    # USER не может удалять фильмы
    def test_delete_movie_forbidden(self, user_session):
        resp = user_session.movies_api.delete_movies_by_id(movie_id=1, expected_status=403)
        print(f'Forbidden DELETE response: {resp.status_code}')
        assert resp.status_code == 403