#-*- coding: utf-8 -*-

# Tweepy module written by Josh Roselin, documentation at https://github.com/tweepy/tweepy
# SQLite3 Tutorial from http://www.python-kurs.eu/sql_python.php
# This Code is inspired by a Stackoverflow thread and the answer of User Balazs
# https://stackoverflow.com/questions/37398609/save-data-to-sqlite-from-tweepy
# Twitter Developer Documentation Streaming https://dev.twitter.com/streaming/reference/post/statuses/filter

import tweepy 
import sqlite3
import sched, time 

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


    def on_status(self, status):
		if "RT @" not in status.text:
			x.execute("""INSERT INTO Twitter(ID, Text, User, Language) VALUES(?,?,?,?)""",
			(status.id, status.text, status.user.id, status.lang))
			conn.commit()   
		
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True
        
#Initialise the Stream
sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))		

#Keywords that we want our stream filter for
keyword_list = ['Trump', 'Obama']

#Function that takes the keywords as a list and runs the stream
def startstream(keywords):
	sapi.filter(track=keywords)

startstream(keyword_list)
