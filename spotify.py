import requests
import sqlite3

SPOTIFY_CLIENT_ID = 'ea8c52c11a734c049732d0964a3a2b20'
SPOTIFY_CLIENT_SECRET = '75b0e9cd76d44493ba52fa96ebdaa41d'
AUTH_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'

class Spotify:
    def __init__(self):
        print("Initializing Spotify API connection...")
        self.auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET,
        })
        self.auth_response_data = self.auth_response.json()
        self.access_token = self.auth_response_data['access_token']
        self.headers = {'Authorization': f'Bearer {self.access_token}'}
        self.conn = sqlite3.connect('artists.db')
        self.cursor = self.conn.cursor()
        print("Spotify API connection initialized.")

    def get_artist_id_name(self, artist_name):
        """
        Get artist id and name
        """
        print(f"Fetching artist ID and name for: {artist_name}")
        normalized_name = artist_name.lower()

        # query database first
        self.cursor.execute('SELECT id, name FROM artists WHERE LOWER(name) = ?', (normalized_name,))
        result = self.cursor.fetchone()
        if result:
            print(f"Found artist in database: {result[1]} (ID: {result[0]})")
            return result[0], result[1]

        # search Spotify API
        try:
            response = requests.get(url=BASE_URL + 'search/', headers=self.headers, params={'q': artist_name, 'type': 'artist'})
            response.raise_for_status()
            data = response.json()
            if not data['artists']['items']:
                print("Artist not found in Spotify API.")
                return None, None

            artist_id = data['artists']['items'][0]['id']
            artist_new_name = data['artists']['items'][0]['name']

            # Insert into database
            self.cursor.execute('INSERT INTO artists (id, name) VALUES (?, ?)', (artist_id, artist_new_name))
            self.conn.commit()
            print(f"Inserted artist into database: {artist_new_name} (ID: {artist_id})")
            return artist_id, artist_new_name
        except Exception as e:
            print(f"Error occurred while fetching artist: {e}")
            return None, None

    def get_artist_releases(self, artist_id):
        """
        Get 5 most recent releases from artist with given id
        """
        print(f"Fetching releases for artist ID: {artist_id}")

        # query database first
        self.cursor.execute('SELECT album_name, release_date, type FROM spotify_releases WHERE artist_id = ? ORDER BY release_date DESC LIMIT 5', (artist_id,))
        result = self.cursor.fetchall()
        if result:
            print("Found releases in database.")
            releases = [{'name': row[0], 'release_date': row[1], 'type': row[2]} for row in result]
            return releases

        print("Releases not found in database. Fetching from Spotify API...")
        # search Spotify API
        try:
            response = requests.get(url=BASE_URL + f'artists/{artist_id}/albums', headers=self.headers, params={'include_groups': 'album,single,appears_on'})
            response.raise_for_status()
            data = response.json()
            sorted_releases = sorted(data['items'], key=lambda item: item['release_date'], reverse=True)[:5]
            releases = [{'name': item['name'], 'release_date': item['release_date'], 'type': item['album_type']} for item in sorted_releases]

            # insert releases into the database
            for release in releases:
                self.cursor.execute('INSERT INTO spotify_releases (artist_id, album_name, release_date, type) VALUES (?, ?, ?, ?)',
                                    (artist_id, release['name'], release['release_date'], release['type']))
            self.conn.commit()
            print("Inserted releases into database.")
            return releases
        except Exception as e:
            print(f"Error occurred while fetching releases: {e}")
            return []

    def close(self):
        self.conn.close()
        print("Database connection closed.")


