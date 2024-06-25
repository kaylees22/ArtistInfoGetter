# set up spotify api connection here
import requests
import json
import os

class Spotify:



    AUTH_URL = 'https://accounts.spotify.com/api/token'

    auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': os.environ.get('SPOTIFY_CLIENT_ID'),
    'client_secret': os.environ.get('SPOTIFY_CLIENT_SECRET'),
    })

    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

    def get_artist(self, artist_name):

        BASE_URL = 'https://api.spotify.com/v1/'
        # track_id = input('Enter track id: ')

        # parse out track id from input url
        url = input('Enter song url: ')
        start = url.index('track') + 2
        track_id = url[start:]

        # make request
        r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

        print(r.json())


        # comma separated list of ids for recommendations
        track_ids = ''
        for i in range(1,6):
            this_id = input('Enter track_id {i}: ')
            track_ids += this_id + ','
