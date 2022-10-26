from client_wrapper import ClientWrapper
import string
import os
from dotenv import load_dotenv
from pathlib import Path


class Main(ClientWrapper):
    _SPOTIFY_WRAPPER = None

    def __init__(self, client_id: string, client_secret: string, *args, **kwargs):
        super().__init__(client_id, client_secret, *args, **kwargs)
        self._SPOTIFY_WRAPPER = ClientWrapper(client_id, client_secret)

    def get_data(self, resource_type='artist'):
        if resource_type is None:
            raise ValueError('You must specify a type of resource.')

        items = []
        next_page = True
        after = None

        while next_page:
            response = self._SPOTIFY_WRAPPER.get_saved_resource(resource_type=resource_type, offset=after)
            returned_data = []

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


dotenv_path = Path('spotify.env')
load_dotenv(dotenv_path=dotenv_path)
main = Main(os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))
albums = main.get_data('episode')
print(albums)
