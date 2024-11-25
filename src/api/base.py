import requests


class RequestBase:
    base_url: str

    def get(self, url: str, params: dict = None, headers: dict = None) -> dict:
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        full_url = self.base_url + url
        response = requests.get(full_url, params=params, headers=headers)

        return response.json()
