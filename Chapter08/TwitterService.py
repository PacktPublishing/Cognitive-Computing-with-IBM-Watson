import tweepy

consumer_key = "fZEQIZmLjfdnMeqI9rIkBCmWh"
consumer_secret = "bJlMR8k9awL5KNzVtSj5A0aLjmtulWQi4Or6J4H6mk8Aod0jYw"
access_token = "3397145679-0qxjHB66sLOXETBSp5k52wNvYvoNKTZ5vOPjYW7"
access_secret = "0KqVTtisBQHrll6dmq56m1usfX2IQigCE2tDmHRjdeAK3"

def tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    tweets200 = [x.text.encode("utf-8") for x in api.user_timeline(screen_name=screen_name, count=200)]
    return "\n".join(tweets200)