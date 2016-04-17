#example of how to extract contents of a twitter list using Tweepy. 

#Results are saved to a binary file (search_output-YYYY-MM-DD.bin), which is then read and printed out.
import os,pickle
import datetime

import tweepy

CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"] 
CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
ACCESS_KEY = os.environ["TWITTER_ACCESS_KEY"]     
ACCESS_SECRET = os.environ["TWITTER_ACCESS_SECRET"]

LIST = "Gord1ei/news-journos"
DATE = datetime.date.today().isoformat()
TWEETS = 15000

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

results = []

with open("search_output-%s.bin"%DATE,"wb") as result_file:
	for page in tweepy.Cursor(api.search,"list:%s since:%s exclude:replies exclude:retweets"%(LIST,DATE)).pages(TWEETS//15): 
		for i,item in enumerate(page):
			results += [item.text]
			print "%d: %s"%(i,results[-1])
			pickle.dump(results[-1],result_file)
			if len(results)==TWEETS: break

		if len(results)==TWEETS: break

with open("search_output-%s.bin"%DATE,"rb") as result_file:
	results = []
	while not result_file.closed:
		try: 
			results += [pickle.load(result_file)]
			print results[-1]
		except EOFError: result_file.close()


	
