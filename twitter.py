import requests
import sqlite3


class Twitter:
    def __init__(self):
        self.url = "https://twitter154.p.rapidapi.com/user/tweets"
        self.headers = {
            "x-rapidapi-key": "89e8d18db2msh750cb1be8006c38p19c402jsne47214e05847",
            "x-rapidapi-host": "twitter154.p.rapidapi.com"
        }
        self.conn = sqlite3.connect('artists.db')
        self.cursor = self.conn.cursor()

    def get_tweets(self, twitter_handle):
        """
        get 5 most recent tweets from given twitter handle
        """
        print(f'Fetching tweets for {twitter_handle}')

        # query database first
        self.cursor.execute('SELECT tweet_id, creation_date, text FROM twitter_tweets WHERE twitter_handle = ? ORDER BY creation_date DESC LIMIT 5', (twitter_handle,))
        result = self.cursor.fetchall()
        if result:
            print("Found tweets in database.")
            tweets = [{'tweet_id': row[0], 'creation_date': row[1], 'text': row[2]} for row in result]
            return tweets
        
        print("Tweets not found in database. Fetching from Twitter API...")
        # search Twitter API
        querystring = {"username": twitter_handle, "limit": "5", "include_replies": "false", "include_pinned": "false"}
        try:
            response = requests.get(self.url, headers=self.headers, params=querystring)
            response.raise_for_status()
            data = response.json()

            tweets = []
            for tweet in data.get('results',[]):
                tweetData = {
                    'tweet_id': tweet['tweet_id'],
                    'creation_date': tweet['creation_date'],
                    'text': tweet['text']
                }
                tweets.append(tweetData)

                self.cursor.execute('INSERT OR IGNORE INTO twitter_tweets (twitter_handle, tweet_id, creation_date, text) VALUES (?, ?, ?, ?)', (twitter_handle, tweetData['tweet_id'], tweetData['creation_date'], tweetData['text']))
            
            self.conn.commit()
            print("Inserted tweets into database.")
            return tweets
        except Exception as e:
            print(f'Error occurred while fetching tweets: {e}')
            return []
    
    def close(self):
        self.conn.close()
        print("Closed database connection")

if __name__ == '__main__':
    pass
    #     twitter = Twitter()
    #     tweets = twitter.get_tweets('Drake')
    #     for tweet in tweets:
    #         print(f"{tweet['creation_date']}: {tweet['text']}")
    #         print("====================================")
    #     twitter.close()