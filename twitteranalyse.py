#-*- coding: utf-8 -*-

# Tweepy module written by Josh Roselin, documentation at https://github.com/tweepy/tweepy
# MySQLdb module written by Andy Dustman, documentation at http://mysql-python.sourceforge.net/MySQLdb.html

"""This Code is inspired by the GeoSearch crawler, written by Chris Cantey
MS GIS/Cartography, University of Wisconsin, https://geo-odyssey.com"""

import tweepy 


# Go to http://dev.twitter.com and create an app. 
# The consumer key and secret as well as the access_token and secret will be generated for you after you register with Twitter Developers
consumer_key = "XXX"
consumer_secret =  "XXX"

access_token = "XXX"
access_token_secret = "XXX"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
	
	def on_status(self, status):
		print(status.text.encode("utf-8"))
		
	def on_error(sefl,status_code):
		if status_code == 420:
			return False 
		
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)

#The following GEBOX_GERMANY comes from a stackoverflow threat link: https://stackoverflow.com/questions/22889122/how-to-add-a-location-filter-to-tweepy-module

GEOBOX_GERMANY = [5.0770049095, 47.2982950435, 15.0403900146, 54.9039819757]

myStream.filter(locations=GEOBOX_GERMANY)
