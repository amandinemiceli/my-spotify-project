from SpotifyWrapper.auth import Auth
import string
import requests


class Base(Auth):
    BASE_URL = 'https://api.spotify.com/v1/'

    def __init__(self, client_id: string, client_secret: string, redirect_uri: string, *args, **kwargs):
        super().__init__(client_id, client_secret, redirect_uri, *args, **kwargs)

        self.authenticate()

    def get_headers(self):
        return {
            'Authorization': f"Bearer {self.access_token}",
            'Content-Type': 'application/json'
        }

    def get_saved_resource(self, resource_type='artist', offset=None):
        if resource_type is None:
            return ValueError('You must provide a resource type.')

        payload = {'limit': 50}

        if resource_type == 'artist':
            payload['type'] = resource_type
            if offset is not None:
                payload['after'] = offset

            response = self.perform_get_request(endpoint="me/following", payload=payload)
        else:
            endpoint = f"me/{resource_type}s"
            if offset is not None:
                payload['offset'] = offset

            response = self.perform_get_request(endpoint=endpoint, payload=payload)

        return response

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
