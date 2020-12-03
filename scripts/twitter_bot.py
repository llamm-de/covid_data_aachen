import tweepy
import json
import re
from datetime import date, datetime
from scraper import scraper
from export_data import export_data


class twitterBot():
    
    def __init__(self, credential_source):
        self.credential_source = credential_source
        self.is_connected = False


    def connect_to_twitter(self):
        if not self.is_connected:
            # Load credentials
            with open(self.credential_source) as file:
                credentials = json.load(file)

            # Establish connection to api
            auth = tweepy.OAuthHandler(credentials["API-key"], credentials["API-key-secret"])
            auth.set_access_token(credentials["Access-token"], credentials["Access-token-secret"])
            self.api = tweepy.API(auth)
            self.is_connected = True
        else:
            raise RuntimeError('Can not connect to twitter! Bot is already connected!')


    def get_user_timeline(self, user_ID, count=100, include_rts=False, tweet_mode='extended'):
        if self.is_connected:
            return self.api.user_timeline(screen_name=user_ID,
                                        count=count,
                                        include_rts = include_rts,
                                        tweet_mode = tweet_mode)
        else:
            raise RuntimeError('Can not get timeline! Bot is not connected to API!')


    def reply_to_tweet(self, message, tweet_id):
        if self.is_connected:
            self.api.update_status(status=message, in_reply_to_status_id=tweet_id)
        else:
            raise RuntimeError('Can not reply to tweet! Bot is not connected to API!')


    def reply_to_tweet_with_media(self, filename, tweet_id, message=''):
        if self.is_connected:
            self.api.update_with_media(filename, status=message, in_reply_to_status_id=tweet_id)
        else:
            raise RuntimeError('Can not reply to tweet! Bot is not connected to API!')

    
    @staticmethod
    def find_tweets_by_pattern(tweets, pattern):
        # Find tweets be predefined regEx pattern
        matching_tweets = []
        regex = re.compile(pattern)

        for tweet in tweets:
                match = regex.search(tweet.full_text)
                if(match):
                    matching_tweets.append(tweet)

        return matching_tweets


    @staticmethod
    def find_tweets_by_date(tweets, date):
        # Find tweets postet on a certain date
        matching_tweets = []

        for tweet in tweets:
            if (date == datetime.date(tweet.created_at)):
                matching_tweets.append(tweet)

        return matching_tweets


if __name__ == "__main__":

    # Connect to API
    CREDFILE = "./twitter_credentials/twitter_credentials.json"
    bot = twitterBot(CREDFILE)  
    bot.connect_to_twitter()
    
    # Get tweets of PresseamtAachen
    userID = 'Mechaniac2'
    tweets = bot.get_user_timeline(userID)

    # Get current date
    curr_date = date.today()
    
    # Analyse tweets
    pattern = "(Corona-Virus|Fälle|Sieben-Tage-Inzidenz)"
    matched_tweets = bot.find_tweets_by_pattern(tweets, pattern)
    matched_tweets = bot.find_tweets_by_date(matched_tweets, curr_date)

    if matched_tweets:
        print('Found matching tweets! Start replying...')
        # Start scraping and evaluation when tweets match
        scraper()
        export_data()

        # Reply to tweet
        # api.update_status(
        #                 status="#InfoTweet",
        #                 in_reply_to_status_id=tweets[0].id,
        #             )
        # API.update_with_media(filename[, status][, in_reply_to_status_id][, lat][, long][, source][, place_id][, file])
    else:
        print('No matching tweets found!')