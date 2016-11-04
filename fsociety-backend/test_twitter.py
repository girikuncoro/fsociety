from twitter import *
import re

#-----------------------------------------------------------------------
# load our API credentials 
#-----------------------------------------------------------------------
config = {}
execfile("config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
	auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))


#-----------------------------------------------------------------------
# perform a basic search 
# Twitter API docs:
# https://dev.twitter.com/docs/api/1/get/search
#-----------------------------------------------------------------------
query = twitter.search.tweets(q="india pakistan AND -filter:retweets", count=100, lang="en")

#-----------------------------------------------------------------------
# How long did this query take?
#-----------------------------------------------------------------------
print "Search complete (%.3f seconds)" % (query["search_metadata"]["completed_in"])

#-----------------------------------------------------------------------
# Loop through each of the results, and print its content.
#-----------------------------------------------------------------------
for result in query["statuses"]:
	tweet = result["text"].replace("#", "").replace("\r", "").replace("\n", "")
	tweet = tweet.lower().strip()
	tweet = re.sub("(@[a-zA-Z0-9]*)", "", tweet)
	tweet = re.sub("(http[^\s]*)", "", tweet)

	print "(%s) %s" % (result["created_at"], tweet)