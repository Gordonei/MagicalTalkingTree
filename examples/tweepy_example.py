import os
import tweepy

CONSUMER_KEY = os.env["TWITTER_CONSUMER_KEY"] 
CONSUMER_SECRET = os.env["TWITTER_CONSUMER_SECRET"]
ACCESS_KEY = os.env["TWITTER_ACCESS_KEY"]     
ACCESS_SECRET = os.env["TWITTER_ACCESS_SECRET"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

results = []
for page in tweepy.Cursor(api.search,"list:Gord1ei/news-journos since:2016-03-07 exclude:replies exclude:retweets").pages():
	for item in page:
		results += item.text

with open("search_output.txt","w") as result_file:
	for r in results: result_file.write(r.encode())
