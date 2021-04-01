import json
import time

import tweepy

from keys import access_token, access_token_secret, consumer_key, consumer_secret

# USER = "Dustin_Michels"
# USER = "jaketapper"
USER = "DaveMichels"


def create_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def limit_handled(cursor):
    while True:
        try:
            yield next(cursor)
        except tweepy.RateLimitError:
            print("> Pausing for 1 min...")
            time.sleep(1 * 60)
        except StopIteration:
            print("Done")
            break


def get_friends(api, user):
    all_friends = []
    for friend in limit_handled(tweepy.Cursor(api.friends, id=user, count=200).items()):
        all_friends.append(friend)
    return all_friends


if __name__ == "__main__":
    api = create_api()
    friends = get_friends(api, USER)
    data = [f._json for f in friends]
    with open(f"../data/twitter_friends/friends_{USER}.json", "w") as f:
        json.dump(data, f)
