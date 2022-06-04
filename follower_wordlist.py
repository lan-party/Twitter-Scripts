import tweepy
import time

consumer_key = "***"
consumer_secret = "***"
access_token = "***"
access_token_secret = "***"
auth = tweepy.OAuth1UserHandler(
   consumer_key, consumer_secret, access_token, access_token_secret
)
auth.secure = True
api = tweepy.API(auth)

# Get list of followers from a specified username
follower_ids = api.get_follower_ids(screen_name='bciwiki')

wordlist = {}

# Get description from user and split into a list of words
for follower_id in follower_ids:
    user=api.get_user(user_id=follower_id)
    print(user.screen_name)
    descwords = user.description
    descwords = descwords.split(" ")
    for descword in descwords:
        descword = descword.lower()
        if descword not in wordlist:
            wordlist[descword] = 0 # Add previously unknown words to list
        wordlist[descword] += 1 # Increment count for every instance of a word
    time.sleep(1.2)

# Write wordlist to file
wl = open("test.txt", "w", encoding="utf-8")
wl.write(str(wordlist))
