#-*- coding: utf-8 -*-
# Word Cloud https://github.com/amueller/word_cloud/blob/master/README.
# SQLite3 Tutorial from http://www.python-kurs.eu/sql_python.php

import sqlite3
import re
import tweepy
import nltk
import operator
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from nltk.tokenize import RegexpTokenizer

connection = sqlite3.connect("GermanParties.db")
cursor = connection.cursor()

consumer_key = "dDg2wPt249fB87CI8SBDXOpet"
consumer_secret =  "YaNJ4iRphKxke41VpohtzVCOr5C55ljYtEbF1vAF93f80thvsl"
access_token = "2859636691-JyxcWeoUrjZc26L1tRL6QQquijNaLDgQ0Wfm0Jt"
access_token_secret = "ZXpYWICZrKZHIs1dBZboZrdBmMSrla0bxqaJRV0X79xj0"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Die am häufigsten auftauchenden Wörter in einer Tagcloud, 0 Text Analyse, 1 Hashtags
def cloud(c, choise):
	c.execute("""SELECT Text, Hashtags
					FROM Twitter """)
	result = c.fetchall()
	text = ""
	for tweet in result:
		text += str(tweet[choise].encode("utf-8"))+ " "
	text = text.lower()
	stopwords = set(STOPWORDS)
	stopword_list_news = ["https", "via","breaking", "com", "de", "news", "co", "amp", "new", "latest"]
	stopword_list_german =["der", "die", "das", "diese", "jene", "und", "oder", "ja", "nein"]
	stopword_list_trump =["trump", "obama", "donald", "realdonaldtrump", "Trump'", "Trump's", "president"]
	
	"""for s in stopword_list_news:
		stopwords.add(s)"""
		
	"""for s in stopword_list_german:
		stopwords.add(s)"""
		
	"""for s in stopword_list_trump:
		stopwords.add(s)"""	
		
	wordcloud = WordCloud(max_font_size=100, stopwords=stopwords).generate(text)
	
	
	plt.figure()
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.show()

#Verteilung der Top 5 Sprachen
def language_analyse(c):
	c.execute(""" SELECT Count(*), Language 
					FROM Twitter
					GROUP BY Language
					ORDER BY Count(*) DESC
					""")
					
	result = c.fetchall()
	languages = []
	counts = []
	
	for i in range (0,10):
		counts.append(result[i][0])
		languages.append(result[i][1])
	labels = languages
	fig1, ax1 = plt.subplots()
	ax1.pie(counts, labels = labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
	ax1.axis("equal")
	
	plt.show()

#Nennt die Tweets auf die mit den Tweets der Datenbasis am häufigsten geantwortet wurde.	
def most_answered_tweet(c):
	c.execute("""	SELECT Count(*), AnswerToTweet
					FROM Twitter
					GROUP BY AnswerToTweet
					HAVING AnswerToTweet != "Null"
					ORDER BY Count(*) DESC
					LIMIT 10""")
	result = c.fetchall()
	
	for l in result:
		print l[0]
		print api.get_status(l[1]).text.encode("utf-8")
		print api.get_status(l[1]).user.screen_name.encode("utf-8")
		print ""


#Nennt die Nutzer auf die mit den Tweets der Datenbank am häufigsten geantwortet wurde.
def most_answered_user(c):
	c.execute("""	SELECT Count(*), AnswerToUser
					FROM Twitter
					GROUP BY AnswerToUser
					HAVING AnswerToUser != "Null"
					ORDER BY Count(*) DESC""")
	result = c.fetchall()
	usernames = []
	counts = []
	percentage = []
	
	for i in range (0,10):
		counts.append(result[i][0])
		usernames.append(api.get_user(result[i][1]).screen_name)
		
	for i in range (0,10):
		percentage.append(float(result[i][0])/float(sum(counts))*100)
	
	labels = usernames
	sizes = counts
	
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels = labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
	ax1.axis("equal")
	plt.show()
	
	print sum(counts)
	print result[0][0]
	

#Die häufigsten Hashtags in einer Liste		 	
def most_common_hashtags(c):
	c.execute("""SELECT Text, Hashtags
					FROM Twitter
					WHERE Language = "en" """)
	result = c.fetchall()
	text = ""
	
	for tweet in result:
		text += str(tweet[1].encode("utf-8")) + " "
	text = text.lower()
	
	tokenizer = RegexpTokenizer(r'\w+')
	words = tokenizer.tokenize(text)
	frequency = nltk.FreqDist(words)
	sorted_frequency = sorted(frequency.items(), key=operator.itemgetter(1))
	for i in range(-1,-50,-1):
		print sorted_frequency[i]	


#Die häufigsten User in einer Liste	
def most_frequent_user(c):
	c.execute("""	SELECT Count(*), User
					FROM Twitter
					GROUP BY User
					ORDER BY Count(*) DESC
					LIMIT 10""")			
	result = c.fetchall()
	
	counts = []
	user = []
	
	for l in result:
		counts.append(l[0])
		user.append(api.get_user(l[1]).screen_name)
		
	
#Die am häufigsten erwähnten Nutzer		
def most_mentioned_user(c):
	c.execute("""	SELECT Mentions
					FROM Twitter
					""")		
	result = c.fetchall()
	text = ""
	user = []
	counts = []
	for tweet in result:
		text += str(tweet[0]) + " "
			
	tokenizer = RegexpTokenizer(r'\w+')
	words = tokenizer.tokenize(text)
	frequency = nltk.FreqDist(words)
	sorted_frequency = sorted(frequency.items(), key=operator.itemgetter(1))
	for i in range(-1,-10,-1):
		counts.append(sorted_frequency[i][1])
		user.append(api.get_user(sorted_frequency[i][0]).screen_name)
		
		
	labels = user
	sizes = counts
	
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, labels = labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
	ax1.axis("equal")
	
	plt.show()
	
		
def sentiment (c):
	c.execute(""" 	SELECT Count(*), Sentiment
					FROM Twitter 
					GROUP BY Sentiment """)
	result = c.fetchall()
	
	for line in result:
		print line
		
language_analyse(cursor)
