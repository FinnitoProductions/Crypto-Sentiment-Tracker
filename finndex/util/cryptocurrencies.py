from enum import Enum


# Represents an enum of several cryptocurrencies corresponding to their ticker symbols.
class Cryptocurrencies(Enum):
    BITCOIN = "BTC"
    ETHEREUM = "ETH"
    BITCOIN_CASH = "BCH"
    RIPPLE = "XRP"
    LITECOIN = "LTC"
    DOGECOIN = "DOGE"
