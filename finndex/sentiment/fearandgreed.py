'''
Extracts data from the Fear and Greed API and displays it instantaneously and provides a historical representation in a dictionary.
'''

import datetime
import json
import pandas as pd

from finndex.util import cryptocurrencies, dateutil, mathutil, webutil

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"

FEAR_AND_GREED_ADDRESS = "https://api.alternative.me/fng/?limit=0&date_format=us"
    
MIN_FEAR_AND_GREED = 0
MAX_FEAR_AND_GREED = 100

# Uses the Fear and Greed API to extract the Fear and Greed value from any given date.
def getFearAndGreed(date):
    timestampFormatted = date.strftime(dateutil.DESIRED_DATE_FORMAT) 
    
    return getAllFearAndGreed()[timestampFormatted]
   
'''
Uses the Fear and Greed API to extract all Fear and Greed values available as a range from 0-1. Returns a dictionary with key as date
and value the Fear and Greed value on that date.
'''
def getAllFearAndGreed():
    fearAndGreedVals = webutil.getPageContent(FEAR_AND_GREED_ADDRESS)
    jsonUnpacked = json.loads(fearAndGreedVals)
    dataArr = jsonUnpacked['data']
    dataDict = {}
    for singleDay in dataArr:
        timestampFormatted = dateutil.convertTimestamp(singleDay['timestamp'], '%m-%d-%Y', dateutil.DESIRED_DATE_FORMAT)
        dataDict[timestampFormatted] = mathutil.map(int(singleDay['value']), MIN_FEAR_AND_GREED, MAX_FEAR_AND_GREED, 0, 1)
        
    return dataDict

def get_all_fg():
    '''
    ' Retrieves all Fear and Greed values available; maps the values into a range from 0-1. Returns a pandas 
    ' DataFrame object containing each daily Fear and Greed value associated with its corresponding timestamp.
    '''
    
    fg_values = json.loads(webutil.getPageContent(FEAR_AND_GREED_ADDRESS))
    
    fg_data_frame = pd.DataFrame(fg_values["data"]).drop(["time_until_update", "value_classification"],axis=1)
    fg_data_frame["timestamp"] = pd.to_datetime(fg_data_frame["timestamp"])
    fg_data_frame["value"] = fg_data_frame.apply(lambda row: mathutil.map(int(row['value']), MIN_FEAR_AND_GREED, MAX_FEAR_AND_GREED, 0, 1),axis=1)
    fg_data_frame.index = fg_data_frame["timestamp"]
    fg_data_frame.index = fg_data_frame.index.rename("date")
      
    return fg_data_frame.drop("timestamp",axis=1)

def get_fg_dates(start_date, end_date, currencies_list=[cryptocurrencies.Cryptocurrencies.BITCOIN]):
    '''
    ' Retrieves the Fear and Greed values (mapped into a range between 0 and 1) between two dates,
    ' inclusive. Although Fear and Greed is not specific to a given cryptocurrency, the returned
    ' dataframe will be associated with all the cryptocurrencies provided in currencies_list to 
    ' adhere to the standardized cryptocurency-specific plotting format. In other words,
    ' the column of values will be replicated, each under the corresponding cryptocurrency.
    ' The outer column of the returned data frame represents the retrieved cryptocurrencies while the inner columns 
    ' represent the retrieved metric (only "FearGreed", in this case).
    ' 
    ' start_date (datetime) - the start date, with month, day, and year provided
    ' end_date (datetime) - the end date, with month, day, and year provided
    ' currencies_list (list) - the list of currencies to associate with the given fear and greed values
    '''
    fg_data_frame = get_all_fg()
    fg_date_filtered = fg_data_frame.loc[(fg_data_frame.index >= start_date) & 
                                     (fg_data_frame.index < end_date)].copy() 
    
    for currency in currencies_list:
        fg_date_filtered[currency.value] = fg_date_filtered["value"]
    fg_date_filtered = fg_date_filtered.drop("value",axis=1)
    fg_date_filtered.columns = pd.MultiIndex.from_product([currencies_list, ["FearGreed"]])

    return fg_date_filtered