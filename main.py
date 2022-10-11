import os
import secrets
import string
import webbrowser
from urllib.parse import urlencode


def get_random_code():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))


class Spotify:
    AUTH_URL = 'https://accounts.spotify.com/authorize?'
    REDIRECT_URL = 'http://my.spotify-project.io/callback'
    AUTH_SCOPE = 'user-read-private user-read-email'

    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')

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

    def run(self):
        self.get_auth_code()


Spotify().run()
