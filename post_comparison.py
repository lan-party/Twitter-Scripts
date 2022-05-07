import requests
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

# Collect list of categorized companies
resp = str(requests.get("https://bciwiki.org/index.php/Category:Companies").content)
resp = resp.split("</th></tr>")[1]
resp = resp.split("</tbody>")[0]
companies = resp.split("<tr>")
companylinks = []
for a in range(1, len(companies)):
    link = companies[a].split('<a href="')[1]
    link = link.split('"')[0]
    link = link.split("index.php/")[1]
    companylinks += [link]

# Remove companies from list that have been posted to twitter
for status in tweepy.Cursor(api.user_timeline, screen_name='@bciwiki', tweet_mode="extended").items():
    link = ""
    if len(status.entities['urls']) > 0:
        print(status.entities['urls'][0]['expanded_url'].split("index.php/")[1])
        link = status.entities['urls'][0]['expanded_url'].split("index.php/")[1]
    else:
        if "Avalon_AI" in companylinks:
            companylinks.pop(companylinks.index("Avalon_AI"))
        if "Aspect_Imaging" in companylinks:
            companylinks.pop(companylinks.index("Aspect_Imaging"))
    if link in companylinks:
        companylinks.pop(companylinks.index(link))

print(companylinks)
