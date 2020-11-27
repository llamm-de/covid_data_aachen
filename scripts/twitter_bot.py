import tweepy
import json
import re
from datetime import date, datetime
from scraper import scraper
from export_data import export_data


def connect_twitter_api(credential_file):
    # Connect to twitter API unsig credentials from json file
    
    # Load credentials
    with open(credential_file) as file:
        credentials = json.load(file)

    # Establish connection to api
    auth = tweepy.OAuthHandler(credentials["API-key"], credentials["API-key-secret"])
    auth.set_access_token(credentials["Access-token"], credentials["Access-token-secret"])
    api = tweepy.API(auth)

    return api


def find_tweets_by_pattern(tweets, pattern):
    # Find tweets be predefined regEx pattern
    matching_tweets = []
    regex = re.compile(pattern)

    for tweet in tweets:
            match = regex.search(tweet.full_text)
            if(match):
                matching_tweets.append(tweet)

    return matching_tweets


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
    api = connect_twitter_api(CREDFILE)    
    
    # Get tweets of PresseamtAachen
    userID = 'Mechaniac2'
    tweets = api.user_timeline(screen_name=userID, 
                           count=100,
                           include_rts = False,
                           tweet_mode = 'extended'
                           )

    # Get current date
    curr_date = date.today()
    
    # Analyse tweets
    pattern = "(Corona-Virus|Fälle|Sieben-Tage-Inzidenz)"
    matched_tweets = find_tweets_by_pattern(tweets, pattern)
    matched_tweets = find_tweets_by_date(matched_tweets, curr_date)

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