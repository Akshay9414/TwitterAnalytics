import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.news_rss
db.news.create_index([("url",pymongo.ASCENDING)],unique=True)






import nltk
import datetime
#sentiment analysis
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sia = SIA()

def sentiment(content):
	if(content):
		pol_score = sia.polarity_scores(content)
		return (round(2.5*(1+pol_score['compound']),2))
	return None







#keywords list
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def getKeywords(text):
	if(text==None):
		return []
	chunked = ne_chunk(pos_tag(word_tokenize(text)))
	prev = None
	continuous_chunk = []
	current_chunk = []
	
	for i in chunked:
		if type(i) == Tree:
			current_chunk.append(" ".join([token for token, pos in i.leaves()]))
		elif current_chunk:
			named_entity = " ".join(current_chunk)
			if named_entity not in continuous_chunk:
				continuous_chunk.append(named_entity)
				current_chunk = []
		else:
			continue

	if(current_chunk):
		named_entity = " ".join(current_chunk)
		if named_entity not in continuous_chunk:
			continuous_chunk.append(named_entity)

	NE = []
	for ne in continuous_chunk:
		NE.extend(ne.split(' '))

	#tokenize
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(text)

	#stopword removal
	stop_words = stopwords.words('english')
	tokens = [token.lower() for token in tokens if (token.lower() not in stop_words and token not in NE)]

	#stemming
	ps = PorterStemmer()
	tokens = [ps.stem(w) for w in tokens]

	continuous_chunk.extend(tokens)

	return continuous_chunk




def get_articles(rss_url):
	NewsFeed = feedparser.parse(rss_url)
	entries = NewsFeed.entries
	articles = []
	for article in entries:
		# print(datetime.datetime.fromtimestamp(mktime(article['published_parsed'])))
		articles.append({'source':"The Times of India",'title':article['title'],'description':article['summary'],'url':article['link'],'publishAt':datetime.datetime.fromtimestamp(mktime(article['published_parsed'])),'sentiment':sentiment(article['summary']),'keywords':getKeywords(article['title'])})
	
	return articles





import feedparser


# print(entries)


from time import mktime
import time

db_news_count = db.news.count()

# top,world,ind,NRI,Education
rss_urls = ["https://timesofindia.indiatimes.com/rssfeedstopstories.cms","https://timesofindia.indiatimes.com/rssfeeds/296589292.cms","https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms","https://timesofindia.indiatimes.com/rssfeeds/7098551.cms","https://timesofindia.indiatimes.com/rssfeeds/913168846.cms"]

while True:
	
	for rss_url in rss_urls:
		articles = get_articles(rss_url)

		db_news_count = db.news.count()

		if(articles):
			try:
				result = db.news.insert_many(articles,ordered=False)
			except pymongo.errors.BulkWriteError as e:
				print(e)
		
		print("new News received: "+str(db.news.count() - db_news_count))
		db_news_count = db.news.count()

	print("END")
	time.sleep(300)


