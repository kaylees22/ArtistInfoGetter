import sqlite3

def setup_database():
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS artists (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        twitter_handle TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS spotify_releases (
        artist_id TEXT,
        album_name TEXT,
        release_date TEXT,
        type TEXT,
        FOREIGN KEY (artist_id) REFERENCES artists (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS twitter_tweets (
        twitter_handle TEXT,
        tweet_id TEXT PRIMARY KEY,
        creation_date TEXT,
        text TEXT,
        FOREIGN KEY (twitter_handle) REFERENCES artists (twitter_handle)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
