import requests
from .exceptions import DATA_FETCHING_FAILURE_EXCEPTION

class ExpandedRequests:
    def __init__(self, headers: dict = {'User-Agent': 'Mozilla/5.0'}) -> None:
        self.headers = headers

    def get(self, *args, **kwargs) -> bytes:
        response = requests.get(*args, **kwargs, headers=self.headers)
        if response.status_code == 200:
            return response.content
        else:
            raise DATA_FETCHING_FAILURE_EXCEPTION
