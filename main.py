from spotify import Spotify
import pandas as pd
import sqlalchemy as db


def display(list_of_dicts):
    
    dataframe = pd.DataFrame.from_records(list_of_dicts) 

    # engine connects to db
    engine = db.create_engine('sqlite:///releases.db')
    dataframe.to_sql('releasesTable', con=engine, if_exists='replace', index=False)


    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT * FROM releasesTable;")).fetchall()
        print(pd.DataFrame(query_result))
    
    return


def main():
    spotify_api = Spotify()
    print('\nWelcome to My Idol Update! Use this tool to see your favorite artist\'s recent releases and tweets\n')

    quit = False
    while not quit:
        
        artist = input("Please enter an artist name or q to quit: ")
        if artist == 'q':
            quit = True
            break
        
        artist_id = spotify_api.get_artist_id(artist)

        # prompt until success
        while artist_id is None:
            artist = input('Sorry. we couldn\'t find that artist. Please enter an artist name or q to quit: ')

            if artist == 'q':
                quit = True
                break

            artist_id = spotify_api.get_artist_id(artist)
        if quit: break
        
        official_name = spotify_api.get_artist_name(artist_id)
        releases = spotify_api.get_artist_releases(artist_id)

        print(f"\n{official_name}'s recent releases")
        separator = ''
        print(separator.join(['-']*(len(official_name) + 18))) # logic to change len of separator based on name length

        display(releases)
        print()
        
    print('Goodbye!\n')
    

if __name__ == '__main__':
    main()