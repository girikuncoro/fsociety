import re

TWEET_IN_PARAGRAPH = 4

def clean(raw_tweets):
    cleaned_tweets = []

    for raw in raw_tweets:
        tweet = raw["text"].replace("#", "").replace("\r", "").replace("\n", "")
        tweet = tweet.lower()
        tweet = re.sub("(@[a-zA-Z0-9]*)", "", tweet)
        tweet = re.sub("(http[^\s]*)", "", tweet)

        cleaned_tweets.append(tweet.strip())

    return cleaned_tweets

def get_paragraph(count, tweets):
	paragraphs = []
	for i in range(count):
		text = ''
		for j in range(TWEET_IN_PARAGRAPH):
			text += tweets.pop()
		paragraphs.append(text)
	return paragraphs
	