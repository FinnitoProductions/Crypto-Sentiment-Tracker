'''
Uses Stanford's NLP library to analyze and the sentiment of a block of text and provides functions to stop and start the
server.
'''

import os

import numpy
from pycorenlp import StanfordCoreNLP


__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"

STANFORD_NLP_LOCATION = '~/stanford-corenlp-4.1.0' # the location of the Stanford NLP library on my computer 
                                                              # (download at https://stanfordnlp.github.io/CoreNLP)
STANFORD_NLP_TIMEOUT = 100000 # the time after which a given NLP request will be killed if not yet complete
STANFORD_NLP_PORT = 9002

MIN_SENTIMENT = 0
MAX_SENTIMENT = 4

DESIRED_ARTICLES = 10

# Starts the Stanford NLP server with a given timeout and port.
def startServer(timeout, port):
   os.popen('cd {}; java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout {} -port {} &>/dev/null'.format(
         STANFORD_NLP_LOCATION, timeout, port)) 

def find_sentiment(text):
   '''
   ' Uses the Stanford NLP library to determine the average sentiment (sentence-wise) of a given block of text in a range from
   ' 0 (Extremely Negative) to 4 (Extremely Positive). 
   '
   ' text (str): the block of text to be analyzed
   '''
   NLP_SERVER_LOCATION = 'http://localhost:{}'.format(STANFORD_NLP_PORT)
   PROPERTIES_DICTIONARY = {'annotators': 'sentiment', 'outputFormat': 'json', 'timeout': STANFORD_NLP_TIMEOUT}
   
   nlp = StanfordCoreNLP(NLP_SERVER_LOCATION)
   result = nlp.annotate(text, properties = PROPERTIES_DICTIONARY)

   sentiments = []
   for sentenceAnalysis in result['sentences']:
      sentimentValue = float(sentenceAnalysis['sentimentValue'])
      sentiments += [sentimentValue]
   return numpy.average(sentiments)

# Displays a sentiment value (0-4) in a convenient gauge format.
def displaySentimentNum(sentimentVal):
    return gauge.Gauge(labels=['Very Negative','Negative','Neutral','Positive', 'Very Positive'], 
      colors=['#c80000','#c84b00','#646400','#64a000', '#00c800'], currentVal=sentimentVal, minVal = MIN_SENTIMENT, maxVal = MAX_SENTIMENT, title='Cryptocurrency Sentiment')

# Computes the sentiment value of a given piece of text and displays it as a gauge.
def displaySentimentTxt(text):
    return displaySentimentNum(findSentiment(text))    

# Kills the server running on a given port. 
def stopServer(port):
   exec('kill $(lsof -ti tcp:{})'.format(port))

def get_nlp_date_range(start_date, end_date, currencies_list):
   '''
   ' Retrieves the 100 most popular articles for each specified cryptocurrency in the given date range.
   ' Computes the average sentiment of the articles for each currency and returns a dataframe where each
   ' column is equal to the currency and the corresponding row to the value.
   '
   ' start_date (datetime) - the start date, with month, day, and year provided
   ' end_date (datetime) - the end date, with month, day, and year provided
   ' currencies_list (list) - the list of currencies to associate with the given fear and greed values
   '''
   currency_frame = pd.DataFrame()

   for currency in currencies_list:
      articles = newsapi.get_everything(q=currency.value.name,
                                         sources='cnn,business-insider',
                                         domains='coindesk.com',
                                         from_param=start_date.strftime("%Y-%m-%d"),
                                         to=end_date.strftime("%Y-%m-%d"),
                                         language='en',
                                         sort_by='popularity',
                                         page_size = DESIRED_ARTICLES)['articles']
      
      article_content = []
      for article in articles:
         source = article['source']['id'] if article['source']['id'] != None else article['source']['name']
         url = article['url']
         source_calls = {'business-insider': webutil.get_business_insider_text, 
                    'cnn': webutil.get_cnn_text,
                    'CoinDesk': webutil.get_coin_desk_text
                   }
      
         article_content += [source_calls[source](url)]
         
      article_frame = pd.DataFrame(article_content)
      sentiment_frame = article_frame.apply(lambda row: nlp.findSentiment(row[0]), axis=1)
      
      currency_frame[currency.value] = [sentiment_frame.mean()]
   return currency_frame
