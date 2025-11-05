from clients.api_manager import ApiManager
from constants import API_URL

class MoviesManager(ApiManager):
    def __init__(self, session):
        super().__init__(session)
        self.base_url = API_URL
        self.movies_endpoint = "/movies"

    def create_movie(self, movie_data):
        """Создание фильма"""
        return self.send_request(
            method="POST",
            endpoint=self.movies_endpoint,
            data=movie_data,
            expected_status=201
        )

    def get_movies(self, params=None):
        """Получение списка фильмов"""
        return self.send_request(
            method="GET",
            endpoint=self.movies_endpoint,
            params=params,
            expected_status=200
        )

    def get_movie_by_id(self, movie_id):
        """Получение фильма по ID"""
        return self.send_request(
            method="GET",
            endpoint=f"{self.movies_endpoint}/{movie_id}",
            expected_status=200
        )

    def update_movie(self, movie_id, update_data):
        """Обновление фильма"""
        return self.send_request(
            method="PATCH",  # Меняем PUT на PATCH
            endpoint=f"{self.movies_endpoint}/{movie_id}",
            data=update_data,
            expected_status=200
        )

    def delete_movie(self, movie_id):
        """Удаление фильма"""
        return self.send_request(
            method="DELETE",
            endpoint=f"{self.movies_endpoint}/{movie_id}",
            expected_status=200
        )