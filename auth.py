import os
from dotenv import load_dotenv
from pathlib import Path
import secrets
import string
import webbrowser
import base64
import requests
from urllib.parse import urlencode


def get_random_code(number):
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(number))


def base64_encode_token(token):
    return base64.b64encode(token.encode()).decode()


class Auth:
    CLIENT_ID = ''
    CLIENT_SECRET = ''

    REDIRECT_URL = 'http://my.spotify-project.io/callback'

    AUTH_URL = 'https://accounts.spotify.com/authorize?'
    AUTH_SCOPE = 'user-follow-read playlist-read-private user-library-read'

    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    REFRESH_TOKEN = ''

    def __init__(self):
        dotenv_path = Path('spotify.env')
        load_dotenv(dotenv_path=dotenv_path)
        self.CLIENT_ID = os.getenv('CLIENT_ID')
        self.CLIENT_SECRET = os.getenv('CLIENT_SECRET')

    def generate_auth_token(self):
        token = self.CLIENT_ID + ':' + self.CLIENT_SECRET
        return base64_encode_token(token)

    def get_auth_code(self):
        state = get_random_code(16)

        auth_headers = {
            'client_id': self.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URL,
            'scope': self.AUTH_SCOPE,
            'response_type': 'code',
            'state': state
        }

        webbrowser.open(self.AUTH_URL + urlencode(auth_headers))

    def get_access_token(self, auth_code):
        headers = {
            'Authorization': 'Basic ' + self.generate_auth_token(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.REDIRECT_URL
        }

        response = requests.post(self.TOKEN_URL, data=payload, headers=headers)
        self.REFRESH_TOKEN = response.json().get('refresh_token')
        return response.json()

    def get_refresh_token(self):
        headers = {
            'Authorization': 'Basic ' + self.generate_auth_token(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.REFRESH_TOKEN
        }

        response = requests.post(self.TOKEN_URL, data=payload, headers=headers)
        return response.json()

