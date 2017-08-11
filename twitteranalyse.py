#-*- coding: utf-8 -*-

# Tweepy module written by Josh Roselin, documentation at https://github.com/tweepy/tweepy
# SQLite3 Tutorial from http://www.python-kurs.eu/sql_python.php
# This Code is inspired by a Stackoverflow thread and the answer of User Balazs
# https://stackoverflow.com/questions/37398609/save-data-to-sqlite-from-tweepy
# Twitter Developer Documentation Streaming https://dev.twitter.com/streaming/reference/post/statuses/filter
# Textblob Documentation https://textblob.readthedocs.io/en/dev/

import tweepy 
import sqlite3
import re
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer



#Connects with the Database, if you haven't any database look at the SQLite 3 Tutorial how to create one using Python
	
conn = sqlite3.connect('GermanParties.db')		
x = conn.cursor()



# Go to http://dev.twitter.com and create an app 
# The consumer key and secret as well as the access_token and secret will be generated for you after you register with Twitter Developers
consumer_key = "Insert Consumer Key"
consumer_secret =  "Insert Consumer Secret"
access_token = "Inser Access Token"
access_token_secret = "Insert Access Token Secret"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
				self.api = api
				super(tweepy.StreamListener, self).__init__()
				self.count = 0

        
	#Where the Magic happens. This Function is triggered every time a tweet (called status) appears.
    def on_status(self, status):
			
				if "RT @" not in status.text:
					
					hashtag = ""
					urls= ""
					mentions = ""
					
					try:										# This block extracts the entities: Hashtags, Links and Mentions
						for h in status.entities["hashtags"]:
							hashtag += h["text"] +" "
						for l in status.entities["urls"]:
							urls += l["expanded_url"] + " "
						for m in status.entities["user_mentions"]:
							mentions += m["id_str"] + " "  
					except:
						pass
					
					#Automated sentiment analysis by textblob library inspired by http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
					text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(status.text.encode("utf-8"))).split())
					analysis = TextBlob(text)
					sentiment = ""
					
					if analysis.sentiment.polarity > 0:
						sentiment = "pos"
					elif analysis.sentiment.polarity == 0:
						sentiment = "neu"
					else:
						sentiment = "neg"
					
					#SQLite Statement. If you want safe any other values it can be changed here, as long as your database is prepared for the new values.
					x.execute("""INSERT INTO Twitter(ID, TimeStamp, User, Text, Hashtags, Links, Mentions, Language, Sentiment, AnswerToTweet, AnswerToUser) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
					(status.id, status.created_at, status.user.id, status.text, hashtag, urls, mentions, status.lang, sentiment,status.in_reply_to_status_id, status.in_reply_to_user_id))
					conn.commit()
					
					self.count += 1
					print self.count
			
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True
        

#Starts the stream and catches possible exceptions that can occur on several tweets.
def startstream(keywords):
	print "Connecting Stream"
	sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
	print "Initialising Stream"	
	while True:
		try:
			sapi.filter(track=keywords)
		except:
			continue


#Some example keyword lists with topics of interest. Feel free to add any Keywords you like
keyword_list_germanparties = ['CDU', 'CSU', 'SPD', 'FDP', 'Die Gruenen', 'Die Linke', 'AFD', 'NPD']
keyword_list_news = ['news', 'breaking', 'eilmeldung']
keyword_list_trump = ['trump', 'obama', 'potus', 'maga']
keyword_list_brexit = ['brexit', 'theresa may']
keyword_list_got = ["Gameofthrones", "Game of Thrones", "#got"]

startstream(keyword_list_germanparties)
