import datetime

from finndex.aggregate import historical, instantaneous
from finndex.util import dateutil

import flask
import flask_restful

HISTORICAL_SENTIMENT_KEY = 'histSentiment'
INSTANTANEOUS_SENTIMENT_KEY = 'instSentiment'

API_OK_VAL = 200
API_FAILED_VAL = 404

class DataInfo(flask_restful.Resource):
   def get(self, data):
      if data == HISTORICAL_SENTIMENT_KEY:
         historicalManager = historical.HistoricalSentimentManager([historical.HistoricalMetricType.FEAR_AND_GREED,
                                                           historical.HistoricalMetricType.TRENDS,
                                                           historical.HistoricalMetricType.BLOCK_COUNT,
                                                           historical.HistoricalMetricType.DAILY_ADDRESSES,
                                                           historical.HistoricalMetricType.TRANSACTION_CNT],
                                                          startDate = dateutil.getCurrentDateTime() - datetime.timedelta(days=60),
                                                          endDate = dateutil.getCurrentDateTime(),
                                                         unweightedKeywordsList=[historical.HistoricalMetricType.PRICE_USD])
         return historicalManager.getHistoricalSentiment(), API_OK_VAL

      elif data == INSTANTANEOUS_SENTIMENT_KEY:
         instantaneousManager = instantaneous.InstantaneousSentimentManager([instantaneous.StaticMetricType.FEAR_AND_GREED, 
                                                       instantaneous.StaticMetricType.TRENDS])
         return instantaneousManager.getReading(), API_OK_VAL

      return "Data type not found.", API_FAILED_VAL

def setupApi(locName):
   app = flask.Flask(locName)
   api = flask_restful.Api(app)

   api.add_resource(DataInfo, "/user/<string:data>")

   return app
