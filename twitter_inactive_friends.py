import tweepy
import time
import math

consumer_key = "***"
consumer_secret = "***"
access_token = "***"
access_token_secret = "***"
auth = tweepy.OAuth1UserHandler(
   consumer_key, consumer_secret, access_token, access_token_secret
)
auth.secure = True
api = tweepy.API(auth)
friends = api.get_friend_ids()
print(len(friends))

print("link, friends, followers, ffratio, posts")
# Print users I follow with a friends/followers ratio < 10% and users with no posts
# Commented out section can be used to filter out users that have followed me back (rate limit slows it down)
for friend in friends:
    try:
        follow = api.get_user(user_id=friend)
        # followed_by = api.get_friendship(source_id=api.get_user(screen_name='bciwiki').id, target_id=follow.id)[0].followed_by
        # if (follow.friends_count == 0 or follow.statuses_count == 0 or (follow.friends_count/follow.followers_count) <= 0.1) and not followed_by:
        if follow.friends_count == 0 or follow.statuses_count == 0 or (follow.friends_count/follow.followers_count) <= 0.1:
            print("https://twitter.com/"+follow.screen_name+", "+str(follow.friends_count)+", "+str(follow.followers_count)+", "+str(round(follow.friends_count/follow.followers_count, 2))+", "+str(follow.statuses_count))
        time.sleep(1.1)
    except Exception:
        time.sleep(901)
        # follow = api.get_user(user_id=friend)
        # followed_by = api.get_friendship(source_id=api.get_user(screen_name='bciwiki').id, target_id=follow.id)[0].followed_by
        if (follow.friends_count == 0 or follow.statuses_count == 0 or (follow.friends_count/follow.followers_count) <= 0.1) and not followed_by:
            print("https://twitter.com/"+follow.screen_name+", "+str(follow.friends_count)+", "+str(follow.followers_count)+", "+str(round(follow.friends_count/follow.followers_count, 2))+", "+str(follow.statuses_count))
