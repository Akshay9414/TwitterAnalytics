import sys
import collections
import json
import time
import random
import traceback
import jsonpatch
import requests
import sseclient
from terminaltables import AsciiTable

import nltk
import requests
import datetime
import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.news_stream
db.news.create_index([("url",pymongo.ASCENDING)],unique=True)

STREAMDATAIO_APP_TOKEN = "YTdhYjg5MjgtMGY2MS00OTVlLThkZjQtMWMwZjlhZWRlMzAx"
NEWSAPI_APP_TOKEN = "ed76ef6934984c8e861740457dd8d92a"
# NEWSAPI_APP_TOKEN = "bc5586a6f9734be9a891ca0b6d06f244"
# NEWSAPI_APP_TOKEN = "88390a3ce2dd4aad8296543c9af1d95c"

NEWS_API = "https://newsapi.org/v2/everything?sources=the-times-of-india,the-hindu&language=en&apiKey={}".format(NEWSAPI_APP_TOKEN)
URL = ("https://streamdata.motwin.net/{}&X-Sd-Token={}".format(NEWS_API, STREAMDATAIO_APP_TOKEN))






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











def print_table(data):
  # Print data as a table
  table_data = []
  for item in data:
      item = collections.OrderedDict(
          sorted(item.items(), key=lambda t: t[0]))
      if len(table_data) == 0:
          table_data.append(item.keys())
      table_data.append(item.values())
  table = AsciiTable(table_data)
  print(table.table)


def run(data, headers, retryCount):

  articles = []
  count = 0

  print(headers)
  try:
      with requests.get(URL, stream=True, headers=headers) as response:
          start = time.time()
          client = sseclient.SSEClient(response)
          for event in client.events():
              if event.event == "data":
                  # initial data load
                  print("Data event received")
                  last_event_id = event.id
                  data = json.loads(event.data)
                  if('articles' in data):
                    for article in data['articles']:
                      authors = []
                      print(article)
                      if(article['author']):
                        authors = getAuthors(article['author'])
                      articles.append({'source':article['source']['name'],'title':article['title'],'description':article['description'],'url':article['url'],'publishAt':datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),'sentiment':sentiment(article['description']),'keywords':getKeywords(article['title']),'authors':authors})
                      # _id = db.news.insert_one({'source':article['source']['name'],'title':article['title'],'description':article['description'],'url':article['url'],'publishAt':datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),'sentiment':sentiment(article['description']),'keywords':getKeywords(article['title']),'authors':authors})
                    try:
                      db.news.insert_many(articles,ordered=False)
                    except pymongo.errors.BulkWriteError as e:
                      print(e)
                    count=count+1
                    print("count: "+str(count))
                    start = time.time()
                  # print_table(data)
                  # for article in data['articles']:
                  #   print(article['publishedAt'])
                  # print_table(data['articles'])

              elif event.event == "patch":
                  elapsed = (time.time()-start)/60
                  print("got after "+str(elapsed)+" minutes")
                  # new data load after first load
                  print("Patch event received")
                  last_event_id = event.id
                  patch = jsonpatch.JsonPatch.from_string(event.data)
                  patch.apply(data, in_place=True)

                  articles = []
                  if('articles' in data):
                    for article in data['articles']:
                      authors = []
                      print(article)
                      if(article['author']):
                        authors = getAuthors(article['author'])
                      articles.append({'source':article['source']['name'],'title':article['title'],'description':article['description'],'url':article['url'],'publishAt':datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),'sentiment':sentiment(article['description']),'keywords':getKeywords(article['title']),'authors':authors})
                      # _id = db.news.insert_one({'source':article['source']['name'],'title':article['title'],'description':article['description'],'url':article['url'],'publishAt':datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),'sentiment':sentiment(article['description']),'keywords':getKeywords(article['title']),'authors':authors})
                    result = ""
                    try:
                      start = time.time()
                      result = db.news.insert_many(articles,ordered=False)
                    except pymongo.errors.BulkWriteError as e:
                      print(e)

                    print("result: "+str(result))
                    print("insert elapsed time: "+str(time.time() - start)+" sec")
                    count=count+1
                    print("count: "+str(count))

                  start = time.time()
                  # for article in data['articles']:
                  #   print(article['publishedAt'])
                  # print_table(data['articles'])

              elif event.event == "error":
                  # error handling
                  print("Error: {}".format(event.data))
                  client.close()

                  err = json.loads(event.data)
                  status = err['status']

                  # status 2001 -> the API had an error, retry can be worthwhile, 
                  # status 2004 -> there was a connection issue with the targeted API server, retry can be worthwhile
                  # status 2008 -> there was an issue while sending the event message from the server, retry can be worthwhile
                  if retryCount < 5 and (status == 2001 or status == 2004 or status == 2008):
                      retryCount = retryCount + 1
                      
                      # reset the server connection
                      retry = 15
                      if event.retry is not None:
                          retry = event.retry / 1000.0

                      # avoid reconnection at the same time in case of parallel connection
                      time.sleep(retry + random.randint(0, 15))

                      # reset a new connection with LastEventID
                      run(data, { 'Last-Event-ID': last_event_id }, retryCount)

              else:
                  print("received unhandled event")
                  client.close()
  except:
      print(traceback.format_exc())

if __name__ == "__main__":
  run([], {}, 0)
