import unittest
from spotify import Spotify

class TestArtistActivity(unittest.TestCase):
    def __init__(self) -> None:
        self.spotify = Spotify()
    
    def test_get_artist_id(self):
        self.assertEqual(self.spotify.get_artist_id('Drake'), '3TVXtAsR1Inumwj472S9r4')
    
    def test_get_artist_releases(self):
        self.assertEqual(
            self.spotify.get_artist_releases('3TVXtAsR1Inumwj472S9r4'),
            [
                ["Family Matters", "2024-05-03", "single"],
                ['Push Ups', '2024-04-19', 'single'],
                ['act ii: date @ 8 (feat. Drake) [remix]', '2024-03-08', 'single'],
                ['For All The Dogs Scary Hours Edition', '2023-11-17', 'album'],
                ['For All The Dogs', '2023-10-06', 'album']
            ]
        )

if __name__ == '__main__':
    unittest.main()

