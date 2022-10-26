from auth import Auth
import string
import requests


class Base(Auth):
    BASE_URL = 'https://api.spotify.com/v1/'

    _TOKEN = None

    def __init__(self, client_id: string, client_secret: string, *args, **kwargs):
        super().__init__(client_id, client_secret, *args, **kwargs)
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret

    @property
    def get_token(self):
        return self._TOKEN

    def get_headers(self):
        token = self.fetch_token()
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def fetch_token(self):
        if self.get_token is None:
            self._TOKEN = Auth(self.CLIENT_ID, self.CLIENT_SECRET).authenticate()

        return self.get_token

    def perform_get_request(self, method="GET", endpoint="/", item_id=None, payload=None):
        if payload is None:
            payload = {}

        headers = self.get_headers()

        url = f"{self.BASE_URL}{endpoint}"
        if item_id is not None:
            url = f"{self.BASE_URL}{endpoint}/{item_id}"

        response = requests.request(method, url, params=payload, headers=headers)

        if response.status_code not in range(200, 299):
            return response.raise_for_status()

        return response.json()
