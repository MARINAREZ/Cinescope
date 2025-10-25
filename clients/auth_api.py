import requests

from custom_requester.custom_requester import CustomRequester
from constants import *

class AuthAPI(CustomRequester):
    """
    Класс для работы с API аутентификации.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL)

    def register_user(self, user_data, expected_status=201):
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя для регистрации.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint="/register",
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status=200):
        """
        Авторизация пользователя.
        :param login_data: Данные для входа (email и password).
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def logout_user(self, expected_status=200):
        """
        Выход пользователя из системы.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint="/auth/logout",
            expected_status=expected_status
        )

    def refresh_token(self, refresh_token, expected_status=200):
        """
        Обновление access token.
        :param refresh_token: Refresh token.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint="/auth/refresh",
            data={"refreshToken": refresh_token},
            expected_status=expected_status
        )

    def get_current_user(self, expected_status=200):
        """
        Получение информации о текущем пользователе.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint="/auth/me",
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=200):
        return self.send_request(
            method="delete",
            endpoint=f"user/{user_id}",
            expected_status = expected_status
        )

