import pytest
import requests
from custom_requester.custom_requester import CustomRequester
from constants import MOVIE_BASE_URL, MOVIES_ENDPOINT

class MoviesApi(CustomRequester):
    """Класс для работы с фильмами"""
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIE_BASE_URL)

    # Создание фильма
    def create_movies(self, movie_data, expected_status=201):
        return self.send_requester(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            json_data=movie_data,
            expected_status=expected_status
        )

    # Получение фильмов
    def get_movies(self, expected_status=200):
        return self.send_requester(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            expected_status=expected_status
        )

    # Получение фильма по ID
    def get_movies_by_id(self, movie_id, expected_status=200):
        return self.send_requester(
            method="GET",
            endpoint=f'{MOVIES_ENDPOINT}/{movie_id}',
            expected_status=expected_status
        )

    # Удаление фильма по ID
    def delete_movies_by_id(self, movie_id, expected_status=200):
        return self.send_requester(
            method="DELETE",
            endpoint=f'{MOVIES_ENDPOINT}/{movie_id}',
            expected_status=expected_status
        )

    # Изменения фильма по ID
    def patch_movies_by_id(self, movie_id, update_movie_data, expected_status=200):
        return self.send_requester(
            method="PATCH",
            endpoint=f'{MOVIES_ENDPOINT}/{movie_id}',
            json_data=update_movie_data,
            expected_status=expected_status
        )