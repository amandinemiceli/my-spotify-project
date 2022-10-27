from SpotifyWrapper.base import Base
import os
from dotenv import load_dotenv
from pathlib import Path


def get_data(spotify_session, resource_type='artist'):
    if resource_type is None:
        raise ValueError('You must specify a type of resource.')

    items = []
    returned_data = []
    next_page = True
    after = None

    while next_page:
        response = spotify_session.get_saved_resource(resource_type=resource_type, offset=after)

        if resource_type == 'artist':
            after = response.get('artists').get('cursors').get('after')
            returned_data += response.get('artists').get('items')
        else:
            after = response.get('offset')
            returned_data += response.get('items')

        if after is None or after == 0:
            next_page = False

        if len(returned_data) > 0:
            for data in returned_data:
                if resource_type != 'artist':
                    data = data.get(f"{resource_type}")
                items.append({'id': data.get('id'), 'name': data.get('name')})

    return items


# Init a Spotify session
dotenv_path = Path('config/spotify.env')
load_dotenv(dotenv_path=dotenv_path)
session = Base(os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))

# Use session to play with Spotify API
artists = get_data(session)
print(artists)
