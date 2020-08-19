import flask
from flask import request, jsonify
import pandas as pd
import finndex
from finndex.aggregate.historical import HistoricalMetricType, HistoricalSentimentManager
from finndex.util.cryptocurrencies import Cryptocurrencies, Stock

app = flask.Flask(__name__, static_url_path='')
app.config["DEBUG"] = True

@app.route('/api/sentiment/coin=<coin_str>')
def get_sentiment_score(coin_str):
    if 'start_date' in request.args:
        start_date = pd.to_datetime(request.args['start_date'])
    else:
        return "Error: No start date field provided. Please specify a start date."

    if 'end_date' in request.args:
        end_date = pd.to_datetime(request.args['end_date'])
    else:
        return "Error: No end date field provided. Please specify an end date."

    if 'metrics' in request.args:
        metrics_strlist = request.args['metrics'].upper().split(',')
    else:
        return "Error: No metrics field provided. Please specify metrics."

    if 'weights' in request.args:
        weights = [float(metric) for metric in request.args['weights'].upper().split(',')]
    else:
        weights = None

    coin = Cryptocurrencies(Stock(coin_str.upper()))
    sentiment = HistoricalSentimentManager( 
                                [HistoricalMetricType[metric] for metric in metrics_strlist], 
                                [coin],
                                start_date, end_date, weights).get_historical_sentiment()[coin]
    sentiment.index = sentiment.index.strftime('%Y-%m-%d')
    return sentiment.to_dict()

@app.route('/api/price/coin=<coin_str>')
def get_price(coin_str):
    if 'start_date' in request.args:
        start_date = pd.to_datetime(request.args['start_date'])
    else:
        return "Error: No start date field provided. Please specify a start date."

    if 'end_date' in request.args:
        end_date = pd.to_datetime(request.args['end_date'])
    else:
        return "Error: No end date field provided. Please specify an end date."

    coin = Cryptocurrencies(Stock(coin_str.upper()))
    sentiment = HistoricalSentimentManager( 
                                [], 
                                [coin],
                                start_date, end_date, []).get_prices()[coin]["PriceUSD"]
    sentiment.index = sentiment.index.strftime('%Y-%m-%d')
    return sentiment.to_dict()


@app.route('/widgets/<path:path>', methods=['GET'])
def file_retrieve(path):
    f = open('widgets/' + str(path), "r")
    return f.read()

app.run(host='0.0.0.0', port='9200')
