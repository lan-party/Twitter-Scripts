import tweepy
import time

# Names collected from LinkedIn, Slack, and other sources
usernames = open("namelist2.txt", "r").read().splitlines()

# Search terms to filter potential users to follow
dorks = ["peripheral nerve", "spinal cord", "electrode array", "medical device", "neuro", "neura", "bci", "brain", "eeg", "mri", "tms", "fnirs", "optogenetics", "consciousness", "transhuman", "cyborg", "psych", "machine learning", "artificial intelligence", "cognitive", "cognition"]

consumer_key = "***"
consumer_secret = "***"
access_token = "***"
access_token_secret = "***"

auth = tweepy.OAuth1UserHandler(
   consumer_key, consumer_secret, access_token, access_token_secret
)

auth.secure = True

api = tweepy.API(auth)
'''
# Select user by username if they exist and filter by dorks
for name in usernames:
    print(name)
    try:
        user = api.get_user(screen_name=name) 
        desc = user.description.lower()
        print(desc)
        for dork in dorks:
            if dork in desc:
                user.follow()
                print("FOLLOWED!")
                time.sleep(1.2)
                break
    except Exception as e:
        print(e)
    time.sleep(1.2)
'''


# Search for users by name and check all results against dork list
for name in usernames:
    print(name)
    try:
        users = api.search_users(name) # Search for
        for user in users:
            desc = user.description.lower()
            print(desc)
            for dork in dorks:
                if dork in desc:
                    if not user.following:
                        user.follow()
                        print(user.screen_name+" - FOLLOWED!")
                        time.sleep(1.2)
                        break
    except Exception as e:
        print(e)
    time.sleep(1.2)
