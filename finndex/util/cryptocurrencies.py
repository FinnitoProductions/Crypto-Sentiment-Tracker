from enum import Enum

class Stock:
    TICKER_DICTIONARY = 
    {
        'BTC': 'Bitcoin',
        'ETH': 'Ethereum',
        'BCH': 'Bitcoin Cash',
        'XRP': 'Ripple',
        'LTC': 'Litecoin',
        'DOGE': 'Dogecoin',
        'XTZ': 'Tezos',
        'KNC': 'Kyber Network',
        'LINK': 'Chainlink',
        'BAT': 'Basic Attention Token'
    }

    def __init__(self, ticker, name = None):
        ''' 
        ' Creates a new stock object given ticker symbol and long-form name.
        ' 
        ' ticker (str): the ticker symbol of the stock (ex.: BTC)
        ' name (str): the long-form name of the stock (ex. Bitcoin)
        '''
        self.ticker = ticker
        if name == None:
            self.name = TICKER_DICTIONARY[ticker]
        else:
            self.name = name

class Cryptocurrencies(Enum):
    '''
    ' Represents an enum of several cryptocurrencies corresponding to their ticker symbols and long-form names.
    '''
    BITCOIN = Stock("BTC")
    ETHEREUM = Stock("ETH")
    BITCOIN_CASH = Stock("BCH")
    RIPPLE = Stock("XRP")
    LITECOIN = Stock("LTC")
    DOGECOIN = Stock("DOGE")
    TEZOS = Stock("XTZ")
    KYBER_NETWORK = Stock("KNC")
    CHAINLINK = Stock("LINK")
    BAT = Stock("BAT")
