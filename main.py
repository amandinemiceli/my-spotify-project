from auth import Auth
import requests


class Spotify(Auth):
    BASE_URL = 'https://api.spotify.com/v1/'
    HEADERS = {'Content-Type': 'application/json'}

    def get_followed_artists(self, after=None):
        endpoint = self.BASE_URL + 'me/following'
        payload = {'type': 'artist', 'limit': 50}

        if after is not None:
            payload['after'] = after

        response = requests.request("GET", endpoint, params=payload, headers=self.HEADERS)
        return response.json()

    def get_artist(self, artist_id):
        endpoint = self.BASE_URL + 'artists/' + str(artist_id)
        response = requests.request("GET", endpoint, params={}, headers=self.HEADERS)
        return response.json()

    def get_saved_tracks(self):
        endpoint = self.BASE_URL + 'me/tracks'
        payload = {'limit': 50}

        response = requests.request("GET", endpoint, params=payload, headers=self.HEADERS)
        return response.json()

    def get_saved_albums(self):
        endpoint = self.BASE_URL + 'me/albums'
        payload = {'limit': 50}

        response = requests.request("GET", endpoint, params=payload, headers=self.HEADERS)
        return response.json()

    def get_saved_shows(self):
        endpoint = self.BASE_URL + 'me/shows'
        payload = {'limit': 50}

        response = requests.request("GET", endpoint, params=payload, headers=self.HEADERS)
        return response.json()

    def get_saved_episodes(self):
        endpoint = self.BASE_URL + 'me/episodes'
        payload = {'limit': 50}

        response = requests.request("GET", endpoint, params=payload, headers=self.HEADERS)
        return response.json()

    def get_auth(self):
        # get authorization code
        Auth.get_auth_code(self)

        auth_code = input("Enter code from redirect URL here: ")

        # exchange authorization code against access token
        response = Auth.get_access_token(self, auth_code)

        #refresh_token = response.get('refresh_token')
        #print('refresh_token: ', refresh_token)

        return response.get('access_token')

    def run(self):
        access_token = self.get_auth()
        self.HEADERS['Authorization'] = 'Bearer ' + access_token

        # retrieve followed artists
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

        # retrieve saved tracks
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

        # retrieve saved albums
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

        # retrieve saved shows
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

        # retrieve saved episodes
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


Spotify().run()
