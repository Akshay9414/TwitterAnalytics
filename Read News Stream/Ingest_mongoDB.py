import nltk
import requests
import datetime
import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.news

# db.news.create_index([("url",pymongo.ASCENDING)],unique=True)
# db.authors.create_index([("name",pymongo.ASCENDING)],unique=True)
# db.keywords.create_index([("word",pymongo.ASCENDING)],unique=True)






#sentiment analysis
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sia = SIA()

def sentiment(content):
	if(content):
		pol_score = sia.polarity_scores(content)
		return (round(2.5*(1+pol_score['compound']),2))
	return None






#author list
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

def getAuthors(text):
    text2 = "By "+text+"."
    chunked = ne_chunk(pos_tag(word_tokenize(text2)))
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

    if not continuous_chunk:
    	if(text.isupper()):
    		return [text]
    	words = text.split(" ")
    	for word in words:
    		if word.isupper():
    			return [word]

    return continuous_chunk







#keywords list
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




# NEWSAPI_APP_TOKEN = "ed76ef6934984c8e861740457dd8d92a"
NEWSAPI_APP_TOKEN = "bc5586a6f9734be9a891ca0b6d06f244"
# NEWSAPI_APP_TOKEN = "88390a3ce2dd4aad8296543c9af1d95c"

NEWSAPI_URL = "https://newsapi.org/v2/everything"

PARAMS = {'sources':'the-times-of-india,the-hindu','language':'en','apiKey': NEWSAPI_APP_TOKEN} 


time = ["T00:00:00Z","T01:00:00Z","T02:00:00Z","T03:00:00Z","T04:00:00Z","T05:00:00Z","T06:00:00Z","T07:00:00Z","T08:00:00Z","T09:00:00Z","T10:00:00Z","T11:00:00Z","T12:00:00Z","T13:00:00Z","T14:00:00Z","T15:00:00Z","T16:00:00Z","T17:00:00Z","T18:00:00Z","T19:00:00Z","T20:00:00Z","T21:00:00Z","T22:00:00Z","T23:00:00Z","T00:00:00Z"]
today = datetime.date.today()

# str(today - datetime.timedelta(days=29))
count = 0
for x in range(1,30):
	date = str(today - datetime.timedelta(days=x))
	for y in range(0,24):
		from_date = date+time[y]
		to_date = date+time[y+1]
		# print(from_date+" to "+to_date)
		PARAMS["from"] = from_date
		PARAMS["to"] = to_date
		r = requests.get(url = NEWSAPI_URL, params = PARAMS) 
		data = r.json()
		articles = []
		print(data)
		if('articles' in data):
			for article in data['articles']:
				authors = []
				print(article)
				if(article['author']):
					authors = getAuthors(article['author'])
				articles.append({'source':article['source']['name'],'title':article['title'],'description':article['description'],'url':article['url'],'publishAt':datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),'sentiment':sentiment(article['description']),'keywords':getKeywords(article['title']),'authors':authors})
				# _id = db.news.insert_one({'source':article['source']['name'],'title':article['title'],'description':article['description'],'url':article['url'],'publishAt':datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),'sentiment':sentiment(article['description']),'keywords':getKeywords(article['title']),'authors':authors})
			db.news.insert(articles)
			count=count+1
			print("count: "+str(count))



  
# # defining a params dict for the parameters to be sent to the API 
# PARAMS = {'sources':'the-times-of-india','language':'en','apiKey': 'ed76ef6934984c8e861740457dd8d92a'} 
# # sending get request and saving the response as response object 
# r = requests.get(url = NEWSAPI_URL, params = PARAMS) 
# # extracting data in json format 
# data = r.json()

# for article in data['articles']:
# 	# print(article['publishedAt'])
# 	authors = []
# 	# print(article['author'])
# 	if(article['author']):
# 		authors = getAuthors(article['author'])
# 		# print(authors)
# 	# print(getKeywords(article['title']))
# 	_id = db.news.insert_one({'source':article['source']['name'],'title':article['title'],'description':article['description'],'url':article['url'],'publishAt':datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),'sentiment':sentiment(article['description']),'keywords':getKeywords(article['title']),'authors':authors})
# 	# print(_id.inserted_id)