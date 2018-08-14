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

STREAMDATAIO_APP_TOKEN = "YTdhYjg5MjgtMGY2MS00OTVlLThkZjQtMWMwZjlhZWRlMzAx"
NEWSAPI_APP_TOKEN = "ed76ef6934984c8e861740457dd8d92a"

NEWS_API = "https://newsapi.org/v2/everything?sources=bbc-news&apiKey={}".format(NEWSAPI_APP_TOKEN)
URL = ("https://streamdata.motwin.net/{}&X-Sd-Token={}".format(NEWS_API, STREAMDATAIO_APP_TOKEN))


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

  print(headers)
  try:
      with requests.get(URL, stream=True, headers=headers) as response:
          client = sseclient.SSEClient(response)
          for event in client.events():
              if event.event == "data":
                  # initial data load
                  print("Data event received")
                  last_event_id = event.id
                  data = json.loads(event.data)
                  # print_table(data)
                  print_table(data['articles'])

              elif event.event == "patch":
                  # new data load after first load
                  print("Patch event received")
                  last_event_id = event.id
                  patch = jsonpatch.JsonPatch.from_string(event.data)
                  patch.apply(data, in_place=True)
                  print_table(data['articles'])

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
