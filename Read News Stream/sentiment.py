#beautiful soup package
import requests
from bs4 import BeautifulSoup

html = requests.get("https://www.seattlepi.com/news/politics/article/AP-sources-Prosecutors-preparing-charges-against-13168729.php")
html_text = BeautifulSoup(html.text)
# extract_text = html_text.find(class_='arti_cont')
final_text = html_text.get_text()
print(final_text);




#sentiment analysis
# import nltk
# nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sia = SIA()
pol_score = sia.polarity_scores("AP sources: Prosecutors preparing charges against Cohen")
# print(pol_score)




#print table using panda
# import pandas as pd
# results = []
# results.append(pol_score)
# results.append(pol_score)
# df = pd.DataFrame.from_records(results)
# print(df.head())