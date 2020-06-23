from enum import Enum

class Stock:
    def __init__(self, ticker, name):
        ''' 
        ' Creates a new stock object given ticker symbol and long-form name.
        ' 
        ' ticker (str): the ticker symbol of the stock (ex.: BTC)
        ' name (str): the long-form name of the stock (ex. Bitcoin)
        '''
        self.ticker = ticker
        self.name = name

class Cryptocurrencies(Enum):
    '''
    ' Represents an enum of several cryptocurrencies corresponding to their ticker symbols and long-form names.
    '''
    BITCOIN = Stock("BTC", "Bitcoin")
    ETHEREUM = Stock("ETH", "Ethereum")
    BITCOIN_CASH = Stock("BCH", "Bitcoin Cash")
    RIPPLE = Stock("XRP", "Ripple")
    LITECOIN = Stock("LTC", "Litecoin")
    DOGECOIN = Stock("DOGE", "Dogecoin")
    TEZOS = Stock("XTZ", "Tezos")
    KYBER_NETWORK = Stock("KNC", "Kyber Network")
    CHAINLINK = Stock("LINK", "Chainlink")
    BAT = Stock("BAT", "Basic Attention Token")
