import pytest

class TestPositiveMovies:

    def test_get_movies_filtered(self, admin_session):
        params = {"genreId": 1, "published": True}
        resp = admin_session.movies_api.get_movies(params=params)
        data = resp.json()["movies"]
        assert resp.status_code == 200
        assert all(movie["genreId"] == 1 and movie["published"] for movie in data)

    def test_get_movie_by_id_existing(self, admin_session, created_movie):
        movie_id = created_movie["id"]
        resp = admin_session.movies_api.get_movie_by_id(movie_id=movie_id)
        data = resp.json()
        assert resp.status_code == 200
        assert data["id"] == movie_id

    def test_get_movie_by_id_not_existing(self, admin_session):
        resp = admin_session.movies_api.get_movie_by_id(movie_id=999999, expected_status=404)
        assert resp.status_code == 404

    def test_post_movies(self, admin_session, movie_data):
        resp = admin_session.movies_api.create_movie(movie_data)
        data = resp.json()
        assert resp.status_code == 201
        assert data["name"] == movie_data["name"]

    def test_patch_movie_by_id(self, admin_session, update_movie_data, created_movie):
        movie_id = created_movie["id"]
        patch_resp = admin_session.movies_api.patch_movie_by_id(
            movie_id=movie_id,
            update_movie_data=update_movie_data,
            expected_status=200
        )
        data = patch_resp.json()
        assert patch_resp.status_code == 200

    def test_delete_movie(self, admin_session, created_movie):
        movie_id = created_movie["id"]
        resp = admin_session.movies_api.delete_movie_by_id(movie_id)
        assert resp.status_code == 200


class TestNegativeMovies:

    def test_create_movie_forbidden(self, user_session, movie_data):
        resp = user_session.movies_api.create_movie(movie_data, expected_status=403)
        assert resp.status_code == 403

    def test_patch_movie_forbidden(self, user_session, admin_session, movie_data, update_movie_data):
        # Создаём фильм админом
        created = admin_session.movies_api.create_movie(movie_data).json()
        movie_id = created["id"]

        resp = user_session.movies_api.patch_movie_by_id(
            movie_id=movie_id,
            update_movie_data=update_movie_data,
            expected_status=403
        )
        assert resp.status_code == 403

    def test_delete_movie_forbidden(self, user_session, admin_session, movie_data):
        # Создаём фильм админом
        created = admin_session.movies_api.create_movie(movie_data).json()
        movie_id = created["id"]

        resp = user_session.movies_api.delete_movie_by_id(movie_id, expected_status=403)
        assert resp.status_code == 403