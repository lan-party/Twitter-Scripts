import requests
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

def getLinks(r):
    orgs = []
    sections = r.split("</h3>")[1:-8]
    for section in sections:
        links = section.split('href="')[1:]
        for link in links:
            if "index.php/" in link:
                orgs += [link.split('"')[0]]
    return orgs

# Collect list of all twitter-linked organizations
resp = str(requests.get("https://bciwiki.org/index.php/Category:Twitter_Accounts").content)
organizations = []

organizations += getLinks(resp)

outof = resp.split("out of ")[1]
outof = float(outof.split(" ")[0])
pagecount = outof/200
pagecount = math.ceil(pagecount)

nextpage = resp.split(') (<a href="')[1]
nextpage = nextpage.split('"')[0]
nextpage = nextpage.replace("amp;", "")
nextpage = nextpage.replace("amp%", "")
while pagecount > 1:
    resp = str(requests.get("https://bciwiki.org"+nextpage).content)
    organizations += getLinks(resp)
    if ') (<a href="' in resp:
        nextpage = resp.split(') (<a href="')[1]
        nextpage = nextpage.split('"')[0]
        nextpage = nextpage.replace("amp;", "")
        nextpage = nextpage.replace("amp%", "")
    pagecount -= 1

# Follow all twitter accounts that haven't been followed
for org in organizations:
    resp = requests.get("https://bciwiki.org"+org).text
    resp = resp.replace("wix", "")
    if "twitter.com/" in resp:
        twitter = resp.split("twitter.com/")[1]
        twitter = twitter.split('"')[0]
        if "?" in twitter:
            twitter = twitter.split("?")[0]
        twitter.replace("#!/", "")
        try:
            user = api.get_user(screen_name=twitter)
            if not user.following:
                user.follow()
                print(org+" - "+twitter+" - FOLLOWED!")
        except Exception:
            print(org+" - "+twitter+" - Twitter Error")
        time.sleep(1.1)

