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

results = 0 
with open("search_output-%s.bin"%DATE,"wb") as result_file:
	#Writing data header
	header = (
		 "ID",
		 "Text",
		 "Latitude",
		 "Longitude",
		 "Time",
		 "Favourites",
		 "Retweets",
		 "Language",
		 "Client",
		 )
	pickle.dump(header,result_file)

	for page in tweepy.Cursor(api.search,"list:%s since:%s exclude:replies exclude:retweets"%(LIST,DATE)).pages(TWEETS//15): 
		for i,item in enumerate(page):
			# Location Data
			loc_long = 0.0 #W-E
			loc_lat = 0.0 #N-S

			# Use Twitter place object to calculate mid-point of area
			if(item.place != None):
				for coord in item.place.bounding_box.coordinates[0]:
					loc_long += coord[0]
					loc_lat += coord[1]
				loc_long = loc_long/len(item.place.bounding_box.coordinates[0])
				loc_lat = loc_lat/len(item.place.bounding_box.coordinates[0])

			result = (
					item.id_str,
					item.text,
					loc_lat,
					loc_long,
					item.created_at.timestamp(),
					item.favorite_count,
					item.retweet_count,
					item.lang,
					item.source, 
					)
			print("%d: %s"%(i,result))
			pickle.dump(result,result_file)
			results += 1 
			if results==TWEETS: break

		if results==TWEETS: break

with open("search_output-%s.bin"%DATE,"rb") as result_file:
	results = []
	while not result_file.closed:
		try: 
			results += [pickle.load(result_file)]
			print(results[-1])
		except EOFError: result_file.close()


	
