import tweepy
import json
import re
from datetime import date, datetime


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

if __name__ == "__main__":

    # Connect to API
    CREDFILE = "./twitter_credentials/twitter_credentials.json"
    api = connect_twitter_api(CREDFILE)    
    
    # Get tweets of PresseamtAachen
    userID = 'PresseamtAachen'
    tweets = api.user_timeline(screen_name=userID, 
                           count=100,
                           include_rts = False,
                           tweet_mode = 'extended'
                           )

    # Get current date
    curr_date = date.today()
    
    # Analyse tweets
    pattern = "(Corona-Virus|Fälle|Sieben-Tage-Inzidenz)"
    regex = re.compile(pattern)

    for tweet in tweets:
        if (curr_date == datetime.date(tweet.created_at)):
            print('Found tweet from today. Check for keywords in text...')
            match = regex.search(tweet.full_text)
            if(match):
                print('Found covid related keywords in tweet!')
                print(tweet.full_text)
