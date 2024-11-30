import tweepy
from main import twitter_login 

api = twitter_login()

def delete_tweets(count):
    tweets = api.user_timeline(count=count)
    deleted_count = 0
    for tweet in tweets:
        try:
            api.destroy_status(tweet.id)
            deleted_count += 1
        except tweepy.TweepError as e:
            print(f"Error deleting tweet {tweet.id}: {e}")
    
    print(f"{deleted_count} tweets deleted.")

def delete_retweets(count):
    retweets = [status for status in api.user_timeline(count=200) if hasattr(status, 'retweeted_status')]
    deleted_count = 0
    for retweet in retweets[:count]:
        try:
            api.destroy_status(retweet.id)
            deleted_count += 1
        except tweepy.TweepError as e:
            print(f"Error deleting retweet {retweet.id}: {e}")
    
    print(f"{deleted_count} retweets deleted.")
