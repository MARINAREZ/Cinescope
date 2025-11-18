import pytest
import requests
from constants import USER_ENDPOINT, AUTH_BASE_URL
from custom_requester.custom_requester import CustomRequester

class UserApi(CustomRequester):
    """Класс для работы с API пользователей"""
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)
        self.session = session

    # Получение информации о пользователе
    def get_user_info(self, user_id, expected_status=200):
        return self.send_requester(
            method="GET",
            endpoint=f"{USER_ENDPOINT}/{user_id}",
            expected_status=expected_status
        )

    # Удаление пользователя
    def delete_user(self, user_id, expected_status=204):
        return self.send_requester(
            method="DELETE",
            endpoint=f"{USER_ENDPOINT}/{user_id}",
            expected_status=expected_status
        )