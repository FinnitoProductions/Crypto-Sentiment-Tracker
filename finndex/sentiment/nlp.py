'''
Uses Stanford's NLP library to analyze and the sentiment of a block of text and provides functions to stop and start the
server.
'''

import os

import numpy
from pycorenlp import StanfordCoreNLP

from finndex.graphing import gauge

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"

STANFORD_NLP_LOCATION = '~/stanford-corenlp-full-2018-10-05/' # the location of the Stanford NLP library on my computer 
                                                              # (download at https://stanfordnlp.github.io/CoreNLP)
STANFORD_NLP_TIMEOUT = 100000 # the time after which a given NLP request will be killed if not yet complete
STANFORD_NLP_PORT = 9002

MIN_SENTIMENT = 0
MAX_SENTIMENT = 4

# Starts the Stanford NLP server with a given timeout and port.
def startServer(timeout, port):
   os.popen('cd {}; java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout {} -port {} &>/dev/null'.format(
         STANFORD_NLP_LOCATION, timeout, port)) 

# Determines the sentiment of a given block of text as a range from 0 (Extremely Negative) to 4 (Extremely Positive).
def findSentiment(text):
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
