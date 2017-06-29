#-*- coding: utf-8 -*-

# Tweepy module written by Josh Roselin, documentation at https://github.com/tweepy/tweepy
# SQLite3 Tutorial from http://www.python-kurs.eu/sql_python.php
# This Code is inspired by a Stackoverflow thread and the answer of User Balazs
# https://stackoverflow.com/questions/37398609/save-data-to-sqlite-from-tweepy
# Twitter Developer Documentation Streaming https://dev.twitter.com/streaming/reference/post/statuses/filter

import tweepy 
import sqlite3
import re
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

#Connect with the Database, if you haven't any database look at the SQLite 3 Tutorial how to create one using Python
conn = sqlite3.connect('Trump.db')
x = conn.cursor()


# Go to http://dev.twitter.com and create an app. 
# The consumer key and secret as well as the access_token and secret will be generated for you after you register with Twitter Developers
consumer_key = "dDg2wPt249fB87CI8SBDXOpet"
consumer_secret =  "YaNJ4iRphKxke41VpohtzVCOr5C55ljYtEbF1vAF93f80thvsl"
access_token = "2859636691-JyxcWeoUrjZc26L1tRL6QQquijNaLDgQ0Wfm0Jt"
access_token_secret = "ZXpYWICZrKZHIs1dBZboZrdBmMSrla0bxqaJRV0X79xj0"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
				self.api = api
				super(tweepy.StreamListener, self).__init__()
				self.count = 0
				self.errorcount = 0

        
	#Where the Magic happens. Function that starts with every incomming tweet (status)
    def on_status(self, status):
			try:
				if "RT @" not in status.text:
					
					hashtag = ""
					try:
						for h in status.entities["hashtags"]:
							hashtag += h["text"] +" "
					except:
						print "No Hashtags used"
					
					text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(status.text.encode("utf-8"))).split())
					analysis = TextBlob(text)
					sentiment = ""
					
					if analysis.sentiment.polarity > 0:
						sentiment = "pos"
					elif analysis.sentiment.polarity == 0:
						sentiment = "neu"
					else:
						sentiment = "neg"
					
					
					x.execute("""INSERT INTO Twitter(ID, TimeStamp, User, Text, Hashtags, Language, Sentiment) VALUES(?,?,?,?,?,?,?)""",
					(status.id, status.created_at, status.user.id, status.text,hashtag, status.lang, sentiment))
					conn.commit()
					
					self.count += 1	
					print self.count, self.errorcount
			except IncompleteRead:
				self.errorcount += 1
			
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True
        
#Initialise the Stream


#Keywords that we want our stream filter for
keyword_list = ['Trump', 'Obama']

#Function that takes the keywords as a list and runs the stream
def startstream(keywords):
	sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))		
	while True:
		try:
			sapi.filter(track=keywords)
		except:
			continue

startstream(keyword_list)
