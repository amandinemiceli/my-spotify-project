# my-spotify-project

 - **SpotifyWrapper** is my own python wrapper for Spotify Web API using the _Authorization flow_.
 - **Main** class implements the SpotifyWrapper for my use case.

## What does the code do?

1. Allow a Spotify user to retrieve followed artists, saved albums, tracks, episodes, shows, etc. from their account 
2. and add them on a new account

## Spotify Web API documentation
https://developer.spotify.com/documentation/web-api/quick-start/

## Usage

SpotifyWrapper can be instantiated this way:
```
session = SpotifyWrapper\Base(client_id, client_secret, redirect_uri)
```

You can then call the wrapper methods to retrieve data from Spotify:
```
session.get_saved_resource(resource_type, offset)
```