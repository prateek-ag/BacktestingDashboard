import sys 
sys.path.append('../backtesting') 

from strategy_interface import StrategyInterface
from typing import Tuple
import numpy as np

class Strategy1(StrategyInterface):

    def __init__(self):
        self.price_hist = list()
        self.ticker = None
        self.thresh = 0.025

    def get_data_fields(self) -> list:
        return ["SMA"]

    def store_ticker_names(self, tickers):
        self.ticker = tickers[0]

    def add_new_price(self, new_price):
        if len(self.price_hist) < 10:
            self.price_hist.append(new_price)
        else:
            self.price_hist.pop(0)
            self.price_hist.append(new_price)

    def step(self, data, stock, cash) -> Tuple[dict, list]:
        curr_price = data[self.ticker].Price
        self.add_new_price(curr_price)

        sma = np.mean(self.price_hist)
        if len(self.price_hist) < 10:
            return (stock, sma)
        else:
            stock = stock[self.ticker]
            new_stock = stock
            if curr_price >= (1 + self.thresh) * sma:
                new_stock = self.sell_stock(stock, cash, curr_price)
            if curr_price <= (1 - self.thresh) * sma:
                new_stock = self.buy_stock(stock, cash, curr_price)

            return ({self.ticker: new_stock}, sma)

    def buy_stock(self, stock, cash, price):
        amount = cash//price
        return stock + amount

    def sell_stock(self, stock, cash, price):
        return 0

    def reset(self):
        pass