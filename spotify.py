import requests
import json
import os
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, AUTH_URL

BASE_URL = 'https://api.spotify.com/v1/'

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



    def get_artist_id(self, artist_name):
        """
        get artist id/info
        """
        
        # search for the artist
        response = requests.get(url=BASE_URL + 'search/',headers = self.headers, params={'q': artist_name, 'type': 'artist'})
        data = response.json()


        return data['artists']['items'][0]['id']
        

    def get_artist_releases(self, id):
        """
            get 5 most recent releases from artist with given id
        """

        response = requests.get(url=BASE_URL + f'artists/{id}/albums',headers = self.headers, params={'include_groups': 'album,single,appears_on'})
        data = response.json()
        
        sorted_releases = sorted(data['items'], key=lambda item: item['release_date'], reverse=True)[:5]
        releases = [[item['name'], item['release_date'], item['album_type']] for item in sorted_releases]

        return releases


if __name__ == '__main__':
    spotify = Spotify()
    spotify.get_artist_releases(spotify.get_artist_id('drake'))
    pass