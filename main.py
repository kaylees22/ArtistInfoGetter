from spotify import Spotify

def main():
    spotify_api = Spotify()

    while True:
        artist = input("Please input an artist name (q to quit): ")
        if artist == 'q':
            break

        artist_id = spotify_api.get_artist_id(artist)
        releases = spotify_api.get_artist_releases(artist_id)

        print(f"Here are {artist}'s recent releases")
        print("---------------------------------------")
        for name, date, type in releases:
            print(f'{name} is a(n) {type} that was released on {date}')
    
    return
    



if __name__ == '__main__':
    main()