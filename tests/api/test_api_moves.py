import pytest
import requests
from constants import API_URL


class TestApiMovies:
    # ПОЗИТИВНЫЕ ТЕСТЫ

    def test_create_movie(self, movies_manager, create_movie_data):
        """Позитивный тест создания фильма"""
        response = movies_manager.create_movie(create_movie_data)
        movie_data = response.json()

        assert movie_data["id"] is not None
        assert movie_data["name"] == create_movie_data["name"]
        assert movie_data["description"] == create_movie_data["description"]
        assert movie_data["price"] == create_movie_data["price"]

        # Cleanup
        movies_manager.delete_movie(movie_data["id"])

    def test_get_movies(self, movies_manager):
        """Позитивный тест получения списка фильмов"""
        response = movies_manager.get_movies()
        movies_data = response.json()

        assert isinstance(movies_data, dict)
        assert "movies" in movies_data
        assert "count" in movies_data
        assert "page" in movies_data
        assert "pageCount" in movies_data
        assert isinstance(movies_data["movies"], list)

    def test_get_movie_by_id(self, movies_manager, created_movie):
        """Позитивный тест получения фильма по ID"""
        movie_id = created_movie["id"]
        response = movies_manager.get_movie_by_id(movie_id)
        movie_data = response.json()

        assert movie_data["id"] == movie_id
        assert movie_data["name"] == created_movie["name"]
        assert "createdAt" in movie_data

    def test_update_movie(self, movies_manager, created_movie):
        """Позитивный тест обновления фильма"""
        movie_id = created_movie["id"]

        update_data = {
            "name": "Обновленное название",
            "description": "Обновленное описание",
            "price": 999,
            "published": False
        }

        # Используем прямой запрос
        response = movies_manager._send_request("PATCH", f"/movies/{movie_id}", data=update_data, expected_status=200)
        updated_movie = response.json()

        assert updated_movie["name"] == update_data["name"]
        assert updated_movie["description"] == update_data["description"]
        assert updated_movie["price"] == update_data["price"]
        assert updated_movie["published"] == update_data["published"]

    def test_delete_movie(self, movies_manager, create_movie_data):
        """Позитивный тест удаления фильма"""
        # Создаем фильм для удаления
        create_response = movies_manager.create_movie(create_movie_data)
        movie_id = create_response.json()["id"]

        # Удаляем фильм
        delete_response = movies_manager.delete_movie(movie_id)
        assert delete_response.status_code == 200

        # Проверяем, что фильм удален
        get_response = movies_manager._send_request("GET", f"/movies/{movie_id}", expected_status=None)
        assert get_response.status_code == 404

    def test_get_movies_with_filters(self, movies_manager):
        """Тест фильтрации фильмов"""
        # Тестируем разные фильтры (основные параметры из Swagger)
        test_cases = [
            {"page": 1, "limit": 5},
            {"page": 2, "limit": 10},
            {"query": "фильм"},
            {"location": "MSK"},
            {"published": "true"}
        ]

        for filters in test_cases:
            response = movies_manager.get_movies(params=filters)
            movies_data = response.json()

            assert response.status_code == 200
            assert isinstance(movies_data, dict)
            assert "movies" in movies_data

    def test_get_movies_pagination(self, movies_manager):
        """Тест пагинации списка фильмов"""
        # Получаем первую страницу
        page1_response = movies_manager.get_movies(params={"page": 1, "limit": 5})
        page1_data = page1_response.json()

        # Получаем вторую страницу
        page2_response = movies_manager.get_movies(params={"page": 2, "limit": 5})
        page2_data = page2_response.json()

        # Проверяем, что страницы разные
        assert page1_data["page"] == 1
        assert page2_data["page"] == 2

    # НЕГАТИВНЫЕ ТЕСТЫ

    def test_create_movie_invalid_data(self, movies_manager):
        """Негативный тест создания фильма с невалидными данными"""
        invalid_data = {
            "name": "",  # Пустое название
            "price": "invalid_price",  # Невалидная цена
            "location": "INVALID",  # Невалидная локация
            "genreId": "invalid"  # Невалидный genreId
        }

        response = movies_manager._send_request("POST", "/movies", data=invalid_data, expected_status=None)
        assert response.status_code in [400, 422]  # Ожидаем ошибку валидации

    def test_get_nonexistent_movie(self, movies_manager):
        """Негативный тест получения несуществующего фильма"""
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        response = movies_manager._send_request("GET", f"/movies/{nonexistent_id}", expected_status=None)
        assert response.status_code in [404, 500]

    def test_update_nonexistent_movie(self, movies_manager):
        """Негативный тест обновления несуществующего фильма"""
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        update_data = {"name": "Новое название"}

        response = movies_manager._send_request("PATCH", f"/movies/{nonexistent_id}", data=update_data,
                                                expected_status=None)
        assert response.status_code == 404

    def test_delete_nonexistent_movie(self, movies_manager):
        """Негативный тест удаления несуществующего фильма"""
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        response = movies_manager._send_request("DELETE", f"/movies/{nonexistent_id}", expected_status=None)
        assert response.status_code == 404

    def test_create_movie_missing_required_fields(self, movies_manager):
        """Негативный тест создания фильма без обязательных полей"""
        incomplete_data = {
            "name": "Фильм без обязательных полей"
        }

        response = movies_manager._send_request("POST", "/movies", data=incomplete_data, expected_status=None)
        assert response.status_code in [400, 422]

    def test_get_movies_invalid_filters(self, movies_manager):
        """Негативный тест с невалидными фильтрами"""
        invalid_filters = {
            "page": -1,  # Невалидная страница
            "limit": 0,  # Невалидный лимит
        }

        response = movies_manager._send_request("GET", "/movies", params=invalid_filters, expected_status=None)
        assert response.status_code == 400

    def test_crud_operations_unauthorized(self):
        """Негативный тест операций без авторизации"""
        unauthorized_session = requests.Session()
        unauthorized_session.headers.update({"Content-Type": "application/json"})

        from clients.movies_manager import MoviesManager
        movies_manager_unauth = MoviesManager(unauthorized_session)

        # Пытаемся создать фильм без авторизации
        response = movies_manager_unauth._send_request("POST", "/movies", data={"name": "Test"}, expected_status=None)
        assert response.status_code == 401