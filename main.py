from auth import Auth
import os
import string
from dotenv import load_dotenv
from pathlib import Path
import requests


class Spotify(Auth):
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

    def perform_get_request(self, method="GET", resource_type="/", item_id=None, payload=None):
        if payload is None:
            payload = {}

        headers = self.get_headers()

        endpoint = f"{self.BASE_URL}{resource_type}"
        if item_id is not None:
            endpoint = f"{self.BASE_URL}{resource_type}/{item_id}"

        response = requests.request(method, endpoint, params=payload, headers=headers)

        if response.status_code not in range(200, 299):
            return response.raise_for_status()
        return response.json()

    def get_followed_artists(self, after=None):
        payload = {'type': 'artist', 'limit': 50}
        if after is not None:
            payload['after'] = after

        return self.perform_get_request(resource_type="me/following", payload=payload)

    def get_artist(self, artist_id):
        return self.perform_get_request(resource_type="artists", item_id={artist_id})

    def get_saved_tracks(self):
        return self.perform_get_request(resource_type="me/tracks", payload={'limit': 50})

    def get_saved_albums(self):
        return self.perform_get_request(resource_type="me/albums", payload={'limit': 50})

    def get_saved_shows(self):
        return self.perform_get_request(resource_type="me/shows", payload={'limit': 50})

    def get_saved_episodes(self):
        return self.perform_get_request(resource_type="me/episodes", payload={'limit': 50})

    def process_followed_artists_response(self):
        artists = []
        next_page = True
        after = None

        while next_page:
            response = self.get_followed_artists(after)
            after = response.get('artists').get('cursors').get('after')
            if response.get('artists').get('total') > 0:
                artists += response.get('artists').get('items')
            if after is None:
                next_page = False

        for artist in artists:
            print(artist.get('id'), artist.get('name'))

    def process_saved_tracks_response(self):
        tracks = []
        next_page = True

        while next_page:
            response = self.get_saved_tracks()
            if response.get('total'):
                tracks += response.get('items')
            if response.get('next') is None:
                next_page = False

        for track in tracks:
            print(track.get('track').get('id'), track.get('track').get('name'))

    def process_saved_albums_response(self):
        albums = []
        next_page = True

        while next_page:
            response = self.get_saved_albums()
            if response.get('total'):
                albums += response.get('items')
            if response.get('next') is None:
                next_page = False

        for album in albums:
            print(album.get('album').get('id'), album.get('album').get('name'))

    def process_saved_shows_response(self):
        shows = []
        next_page = True

        while next_page:
            response = self.get_saved_shows()
            if response.get('total'):
                shows += response.get('items')
            if response.get('next') is None:
                next_page = False

        for show in shows:
            print(show.get('show').get('id'), show.get('show').get('name'))

    def process_saved_episodes_response(self):
        episodes = []
        next_page = True

        while next_page:
            response = self.get_saved_episodes()
            if response.get('total'):
                episodes += response.get('items')
            if response.get('next') is None:
                next_page = False

        for episode in episodes:
            print(episode.get('episode').get('id'), episode.get('episode').get('name'))


dotenv_path = Path('spotify.env')
load_dotenv(dotenv_path=dotenv_path)
spotify = Spotify(os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))
spotify.process_saved_albums_response()
