import sqlite3
connection = sqlite3.connect("Trump.db")

cursor = connection.cursor()

cursor.execute("SELECT Text FROM Twitter")

result = cursor.fetchall()
tweets = []

for r in result:
	tweets.append(str(r))
count = 0

for t in tweets:
	if "Trump" in t:
		print "Found Trump"
		count+=1
	else:
		print "Trump's hiding"

print len(tweets)
print count
