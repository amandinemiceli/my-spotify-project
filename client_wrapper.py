from base import Base
import string


class ClientWrapper(Base):

    def __init__(self, client_id: string, client_secret: string, *args, **kwargs):
        super().__init__(client_id, client_secret, *args, **kwargs)
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret

    def get_artist(self, artist_id):
        return self.perform_get_request(resource_type="artists", item_id={artist_id})

    def get_saved_resource(self, resource_type='artist', offset=None):
        if resource_type is None:
            return ValueError('You must provide a resource type.')

        response = None
        payload = {'limit': 50}

        if resource_type == 'artist':
            payload['type'] = resource_type
            if offset is not None:
                payload['after'] = offset

            response = Base.perform_get_request(self, endpoint="me/following", payload=payload)
        else:
            endpoint = f"me/{resource_type}s"
            if offset is not None:
                payload['offset'] = offset

            response = Base.perform_get_request(self, endpoint=endpoint, payload=payload)

        return response
