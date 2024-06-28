from spotify import Spotify
from twitter import Twitter
import pandas as pd

def display(list_of_dicts):
    """
    Display the list of dictionaries in a tabular format using pandas
    """
    dataframe = pd.DataFrame.from_records(list_of_dicts)
    print(dataframe)

def main():
    spotify_api = Spotify()
    twitter_api = Twitter()
    print("\nWelcome to My Idol Update! Use this tool to see your favorite artist's recent releases and tweets\n")

    while True:
        artist = input("Please enter an artist name or q to quit: ").strip()
        if artist.lower() == 'q':
            break
        
        artist_id, official_name = spotify_api.get_artist_id_name(artist)
        
        # Prompt until success
        while artist_id is None:
            artist = input("Sorry, we couldn't find that artist. Please enter another artist name or q to quit: ").strip()
            if artist.lower() == 'q':
                break
            artist_id, official_name = spotify_api.get_artist_id_name(artist)
        if artist.lower() == 'q':
            break

        if artist_id:
            try:
                releases = spotify_api.get_artist_releases(artist_id)
                if releases:
                    print(f"\n{official_name}'s recent releases")
                    separator = '-' * (len(official_name) + 18)
                    print(separator)
                    display(releases)
                else:
                    print(f"No recent releases found for {official_name}.")
            except Exception as e:
                print(f"Error occurred while fetching releases: {e}")
        else:
            print(f"Artist {artist} not found.")


        """
        check if twitter handle in database
            if not
                find twitter handle using chatgpt
                if chatgpt cant find it, prompt the user to enter it or skip

            
        return twitter handle
        
        """

        # set to drake for testing
        twitter_handle = "Drake"
        # get tweets
        if twitter_handle:
            try:
                tweets = twitter_api.get_tweets(twitter_handle)
                if tweets:
                    print(f"\n{official_name}'s recent tweets")
                    separator = '-' * (len(official_name) + 15)
                    print(separator)
                    display(tweets)
                else:
                    print(f"No recent tweets found for {official_name}.")
            except Exception as e:
                print(f"Error occurred while fetching tweets: {e}")
        else:
                print(f"No Twitter handle provided for {official_name}.")
        
    print('Goodbye!\n')
    spotify_api.close()

if __name__ == '__main__':
    main()
