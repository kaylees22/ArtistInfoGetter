import requests
import json
import os
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, AUTH_URL

class Spotify:
    def __init__(self) -> None:
        self.auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': SPOTIFY_CLIENT_ID,
    'client_secret': SPOTIFY_CLIENT_SECRET,
    })
        self.auth_response_data = self.auth_response.json()
        self.access_token = self.auth_response_data['access_token']
        self.headers = {'Authorization': 'Bearer {token}'.format(token=self.access_token)}

    # get artist id/info
    def get_artist_id(self, artist_name):
        BASE_URL = 'https://api.spotify.com/v1/'
        # track_id = input('Enter track id: ')
        
        # search for the artist
        response = requests.get(BASE_URL + 'search',header=self.headers, params={'q': artist_name, 'type': 'artist'})
        data = response.json()

        print(data)



        # # parse out track id from input url
        # url = input('Enter song url: ')
        # start = url.index('track') + 2
        # track_id = url[start:]

        # # make request
        # r = requests.get(BASE_URL + 'browse/new-releases' + track_id, headers=self.headers)

        # print(r.json())


        # # comma separated list of ids for recommendations
        # track_ids = ''
        # for i in range(1,6):
        #     this_id = input('Enter track_id {i}: ')
        #     track_ids += this_id + ','

    # get artist recent releases


def main():
    spotify = Spotify()
    print("test")
    pass