import sqlite3
import re
import nltk
import operator
from nltk.tokenize import RegexpTokenizer
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

connection = sqlite3.connect("Trump.db")
hashtag_cursor = connection.cursor()
text_cursor = connection.cursor()


hashtag_cursor.execute("""SELECT Hashtags, Sentiment From Twitter WHERE Language = "en" and Sentiment <> "Null" """)
text_cursor.execute("""SELECT Text, Sentiment From Twitter WHERE Language = "en" and Sentiment <> "Null" """)

result = hashtag_cursor.fetchall()
textresult = text_cursor.fetchall()



	
#returns long string containing all hashtags
def get_hashtags(sentiment):
	hashtags = ""
	if sentiment == "all":
		for tweet in result:
			hashtags +=  tweet[0].encode("utf-8")
	else:
		for tweet in result:
			if tweet[1] == sentiment:
				hashtags +=  tweet[0].encode("utf-8")
	
	return hashtags.lower()

def get_hashtag_frequency (hashtag_string):
	tokenizer = RegexpTokenizer(r'\w+')
	words = tokenizer.tokenize(hashtag_string)
	frequency = nltk.FreqDist(words)
	sorted_frequency = sorted(frequency.items(), key=operator.itemgetter(1))
	return sorted_frequency

text = ""
for tweet in textresult:
			text +=  tweet[0].encode("utf-8").lower()
			
frq = get_hashtag_frequency (text)

for i in range (-1,-100,-1):
	print frq[i]

"""
allh = get_hashtags("all")
posh = get_hashtags("pos")
neuh = get_hashtags("neu")
negh = get_hashtags("neg")

allfreq = get_hashtag_frequency(allh)
posfreq = get_hashtag_frequency(posh)
neufreq = get_hashtag_frequency(neuh)
negfreq = get_hashtag_frequency(negh)

for i in range(-1,-11,-1):
	print "All Hash ", i*-1, allfreq[i]
	print "Good Hash ", i*-1, posfreq[i]
	print "Neutral Hash ", i*-1, neufreq[i]
	print "Negative Hash ", i*-1, negfreq[i]
	print ""
	"""
	
