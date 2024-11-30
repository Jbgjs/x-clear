import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET = os.getenv('TWITTER_API_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

def authenticate_twitter(api_key, api_secret, access_token, access_secret):
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    return tweepy.API(auth)

api = authenticate_twitter(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

def get_pinned_tweet_id(api, username):
    try:
        user = api.get_user(screen_name=username)
        return user.pinned_tweet_id if user.pinned_tweet_id else None
    except tweepy.TweepyException as e: 
        print(f"Error fetching pinned tweet for {username}: {e}")
        return None

def delete_tweets(api, username, num_tweets_to_delete):
    pinned_tweet_id = get_pinned_tweet_id(api, username)
    
    tweets = api.user_timeline(screen_name=username, count=num_tweets_to_delete, tweet_mode="extended")
    deleted_count = 0

    for tweet in tweets:
        if tweet.id != pinned_tweet_id:
            try:
                api.destroy_status(tweet.id)
                deleted_count += 1
            except tweepy.TweepyException as e:
                print(f"Error deleting tweet {tweet.id}: {e}")
    
    # 삭제 완료 메시지 출력
    if deleted_count > 0:
        print(f"개발자 닉네임 @CPA286이 만든 트위터 게시글 제거 프로그램입니다. 요청하신 사항을 완료 했습니다.")
    else:
        print("삭제할 게시글이 없습니다.")

def twitter_login():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    try:
        auth_url = auth.get_authorization_url()
        print("Please go to this URL and authorize the app:", auth_url)

        verifier = input("Enter the verification code from the URL: ")
        auth.get_access_token(verifier)

        api = tweepy.API(auth)
        print("Authentication successful!")
        return api
    except tweepy.TweepyException as e:
        print(f"Error during authentication: {e}")
        return None

def main():
    api = twitter_login()
    if api:
        # 게시글 삭제 (예시로 100개의 트윗을 삭제)
        delete_tweets(api, "@CPA286", 100)  
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()
