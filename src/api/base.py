import requests

from src.exceptions import APIFetchException


class RequestBase:
    base_url: str

    def get(self, url: str, params: dict = None, headers: dict = None) -> dict:
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        full_url = self.base_url + url
        try:
            response = requests.get(full_url, params=params, headers=headers)
            return response.json()
        except Exception:
            raise APIFetchException("не удалось подключиться к серверу")
