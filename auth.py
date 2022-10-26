import secrets
import string
import webbrowser
import base64
import datetime
import requests
from urllib.parse import urlencode


class Auth(object):
    REDIRECT_URL = 'http://my.spotify-project.io/callback'

    AUTH_URL = 'https://accounts.spotify.com/authorize?'
    AUTH_SCOPE = 'user-follow-read playlist-read-private user-library-read'

    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    _ACCESS_TOKEN = None
    _REFRESH_TOKEN = None
    _ACCESS_TOKEN_EXPIRED = True

    def __init__(self, client_id: string, client_secret: string, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._CLIENT_ID = client_id
        self._CLIENT_SECRET = client_secret

    @property
    def client_id(self):
        return self._CLIENT_ID

    @property
    def client_secret(self):
        return self._CLIENT_SECRET

    @property
    def access_token(self):
        return self._ACCESS_TOKEN

    @property
    def refresh_token(self):
        return self._REFRESH_TOKEN

    @property
    def has_access_token_expired(self):
        return self._ACCESS_TOKEN_EXPIRED

    @staticmethod
    def get_random_code(number: int):
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(number))

    @staticmethod
    def base64_encode(credentials: string):
        return base64.b64encode(credentials.encode()).decode()

    def get_auth_code(self):
        state = self.get_random_code(16)

        auth_headers = {
            'client_id': self.client_id,
            'redirect_uri': self.REDIRECT_URL,
            'scope': self.AUTH_SCOPE,
            'response_type': 'code',
            'state': state
        }

        webbrowser.open(self.AUTH_URL + urlencode(auth_headers))

    def generate_auth_token(self):
        client_id = self.client_id
        client_secret = self.client_secret

        if client_id is None or client_secret is None:
            raise ValueError('Please provide with valid client_id and client_secret')
        credentials = f"{client_id}:{client_secret}"

        return self.base64_encode(credentials)

    def get_token_headers(self):
        token = self.generate_auth_token()
        return {
            'Authorization': 'Basic ' + token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def get_refresh_token_payload(self):
        return {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

    def get_access_token_payload(self, auth_code: string):
        return {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.REDIRECT_URL
        }

    def get_access_token(self, auth_code=None):
        if self.access_token is None:
            if auth_code is None:
                raise ValueError('You must provide an authorization code to fetch the access token.')
            self.fetch_access_token(auth_code)
            return self.get_access_token()

        if self.has_access_token_expired:
            self.fetch_access_token(refresh=True)
            return self.get_access_token()

        return self.access_token

    def fetch_access_token(self, auth_code=None, refresh=False):
        if auth_code is None and refresh is False:
            raise ValueError('An auth code is required to fetch access token.')

        headers = self.get_token_headers()
        if refresh:
            payload = self.get_refresh_token_payload()
            if self.refresh_token is None:
                raise ValueError('A refresh token is required to fetch a refreshed access token.')
        else:
            payload = self.get_access_token_payload(auth_code)

        response = requests.post(self.TOKEN_URL, data=payload, headers=headers)
        return self.process_response(response)

    def process_response(self, response):
        if response.status_code != 200:
            return response.raise_for_status()

        data = response.json()
        now = datetime.datetime.now()
        expires_at = now + datetime.timedelta(seconds=data.get('expires_in'))

        self._ACCESS_TOKEN_EXPIRED = expires_at < now
        self._ACCESS_TOKEN = data.get('access_token')
        self._REFRESH_TOKEN = data.get('refresh_token')

        return True

    def authenticate(self):
        # get authorization code
        self.get_auth_code()
        auth_code = input("Enter code from redirect URL here: ")

        # exchange authorization code against access token
        return self.get_access_token(auth_code)
