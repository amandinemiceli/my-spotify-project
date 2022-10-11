import os
import secrets
import string
import webbrowser
import base64
import requests
from urllib.parse import urlencode


def get_random_code():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))


def base64_encode_token(token):
    return base64.b64encode(token.encode()).decode()


class Spotify:
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    REDIRECT_URL = 'http://my.spotify-project.io/callback'

    AUTH_URL = 'https://accounts.spotify.com/authorize?'
    AUTH_SCOPE = 'user-read-private user-read-email'

    TOKEN_URL = 'https://accounts.spotify.com/api/token'

    def get_auth_code(self):
        state = get_random_code()

        auth_headers = {
            'client_id': self.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URL,
            'scope': self.AUTH_SCOPE,
            'response_type': 'code',
            'state': state
        }

        webbrowser.open(self.AUTH_URL + urlencode(auth_headers))

    def get_auth_token(self, auth_code):
        token = self.CLIENT_ID + ':' + self.CLIENT_SECRET
        base64_token = base64_encode_token(token)

        headers = {
            'Authorization': 'Basic ' + base64_token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.REDIRECT_URL
        }

        response = requests.post(self.TOKEN_URL, data=payload, headers=headers)
        return response.json()

    def run(self):
        # get authorization code
        self.get_auth_code()

        auth_code = input("Enter code from redirect URL here: ")

        # exchange authorization code against access token
        response = self.get_auth_token(auth_code)
        access_token = response.get('access_token')
        print(access_token)


Spotify().run()
