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

# Search terms to filter potential users to follow
dorks = ["peripheral nerve", "spinal cord", "electrode array", "medical device", "neuro", "neura", "bci", "brain", "eeg", "mri",
         "tms", "fnirs", "optogenetics", "consciousness", "psych", "cognitive", "cognition"]

ignorelist = open("ignorelist.txt", "r")
ignorelisttext = ignorelist.read()
ignorelist.close()

username = 'bciwiki'
follower_ids = api.get_follower_ids(screen_name=username)
follower_ids.reverse()

# Get the followers of all users currently following username
for follower_id in follower_ids:
    ignorelist = open("ignorelist.txt", "a+")
    try:
        # Get more follower info
        follower = user=api.get_user(user_id=follower_id)
        if follower.screen_name not in ignorelisttext:
            
            # Add to ignorelist after checking followers
            follower_followers = api.get_follower_ids(screen_name=follower.screen_name)
            print("SAVE STATE: "+follower.screen_name)
            print(len(follower_followers))
            
            for follower_follower_id in follower_followers:
                # Check if user has been recorded already
                userlist = open("users.tsv", "r", encoding="utf-8")
                if "\n"+str(follower_follower_id)+"\t" not in userlist.read():
                    userlist = open("users.tsv", "a", encoding="utf-8")
                    
                    # Get more info on the followers of each follower
                    follower_follower = api.get_user(user_id=follower_follower_id)
                    for dork in dorks:
                        if follower_follower.followers_count > 0 and follower_follower.friends_count > 0:
                            
                            # Check user descriptions for wordlist matches and check that the user follows the same or more users that follow them
                            if dork in follower_follower.description and (follower_follower.friends_count/follower_follower.followers_count) > 1 and not follower_follower.following and follower_follower.screen_name != username:

                                # Uncomment the next line to automatically follow all matching users
                                #follower_follower.follow()

                                # Add id, username, description, and ffratio to userlist
                                desc = follower_follower.description.encode('unicode-escape').decode('utf-8')
                                desc = desc.replace("\n", "\\n")
                                desc = desc.replace("\t", "\\t")
                                userlist.write(str(follower_follower_id)+"\t"+follower_follower.screen_name+"\t"+desc+"\t"+str(round(follower_follower.friends_count/follower_follower.followers_count))+"\n")
                                print(str(follower_follower_id)+"\t"+follower_follower.screen_name+"\t"+desc+"\t"+str(round(follower_follower.friends_count/follower_follower.followers_count)))
                                break
                    time.sleep(1.2)
                userlist.close()
            ignorelist.write(follower.screen_name+", ")
            time.sleep(1.2)
    except Exception as e:
        ignorelist.write(follower.screen_name+", ")
        input(e)
    ignorelist.close()
