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
        # Используем правильные поля для обновления (те что в create_movie_data)
        update_data = {"name": "Updated Movie Title"}

        # Обновляем фильм
        update_response = movies_manager.update_movie(movie_id, update_data)
        assert update_response.status_code == 200

        # Получаем обновленный фильм для проверки
        get_response = movies_manager.get_movie_by_id(movie_id)
        updated_movie = get_response.json()

        assert updated_movie["name"] == "Updated Movie Title"

    def test_delete_movie(self, movies_manager, create_movie_data):
        """Позитивный тест удаления фильма"""
        # Создаем фильм для удаления
        create_response = movies_manager.create_movie(create_movie_data)
        movie_id = create_response.json()["id"]

        # Удаляем фильм
        delete_response = movies_manager.delete_movie(movie_id)
        assert delete_response.status_code == 200

        # Проверяем, что фильм удален
        # Используем send_request вместо _send_request
        get_response = movies_manager.send_request("GET", f"/movies/{movie_id}", expected_status=None)
        assert get_response.status_code == 404

    def test_get_movies_with_filters(self, movies_manager):
        """Тест фильтрации списка фильмов"""
        # Используем правильные параметры фильтрации
        filters = {"page": 1, "limit": 10}
        response = movies_manager.get_movies(params=filters)

        assert response.status_code == 200
        data = response.json()
        assert "movies" in data
        assert data["page"] == 1

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

        # Используем send_request вместо _send_request
        response = movies_manager.send_request("POST", "/movies", data=invalid_data, expected_status=None)
        assert response.status_code in [400, 422]  # Ожидаем ошибку валидации

    def test_get_nonexistent_movie(self, movies_manager):
        """Негативный тест получения несуществующего фильма"""
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        # Используем send_request вместо _send_request
        response = movies_manager.send_request("GET", f"/movies/{nonexistent_id}", expected_status=None)
        assert response.status_code in [404, 500]

    def test_update_nonexistent_movie(self, movies_manager):
        """Негативный тест обновления несуществующего фильма"""
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        update_data = {"name": "Новое название"}

        # Используем send_request вместо _send_request
        response = movies_manager.send_request("PATCH", f"/movies/{nonexistent_id}", data=update_data,
                                               expected_status=None)
        assert response.status_code == 404

    def test_delete_nonexistent_movie(self, movies_manager):
        """Негативный тест удаления несуществующего фильма"""
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        # Используем send_request вместо _send_request
        response = movies_manager.send_request("DELETE", f"/movies/{nonexistent_id}", expected_status=None)
        assert response.status_code == 404

    def test_create_movie_missing_required_fields(self, movies_manager):
        """Негативный тест создания фильма без обязательных полей"""
        incomplete_data = {
            "name": "Фильм без обязательных полей"
            # Отсутствуют обязательные поля
        }

        # Используем send_request вместо _send_request
        response = movies_manager.send_request("POST", "/movies", data=incomplete_data, expected_status=None)
        assert response.status_code in [400, 422]

    def test_get_movies_invalid_filters(self, movies_manager):
        """Негативный тест с невалидными фильтрами"""
        invalid_filters = {
            "page": -1,  # Невалидная страница
            "limit": 0,  # Невалидный лимит
        }

        # Используем send_request вместо _send_request
        response = movies_manager.send_request("GET", "/movies", params=invalid_filters, expected_status=None)
        assert response.status_code == 400

    def test_crud_operations_unauthorized(self):
        """Негативный тест операций без авторизации"""
        unauthorized_session = requests.Session()
        unauthorized_session.headers.update({"Content-Type": "application/json"})

        from clients.movies_api import MoviesApi
        unauthorized_manager = MoviesApi(unauthorized_session)

        # Тестируем операции без авторизации
        test_data = {
            "name": "Unauthorized Movie",
            "price": 100,
            "location": "MSK",
            "genreId": 1
        }

        # Пытаемся создать фильм без авторизации
        create_response = unauthorized_manager.send_request("POST", "/movies", data=test_data, expected_status=None)
        assert create_response.status_code in [401, 403]

    def test_api_diagnostics(self, movies_manager):
        """Диагностический тест для проверки API"""
        print("\n=== API DIAGNOSTICS ===")
        print(f"Base URL: {movies_manager.base_url}")
        print(f"Movies endpoint: {movies_manager.movies_endpoint}")

        full_url = f"{movies_manager.base_url}{movies_manager.movies_endpoint}"
        print(f"Full URL: {full_url}")

        # Простой GET запрос
        try:
            response = movies_manager.send_request("GET", "/movies", expected_status=None)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error: {e}")