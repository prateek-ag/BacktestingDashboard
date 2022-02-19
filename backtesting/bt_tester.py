import sys 
from backtester import BackTester
from strategies.strategy1 import Strategy1
import yfinance as yf
import pandas as pd


if __name__ == "__main__":
    data = yf.Ticker("msft").history(period="max")
    data_dict = {"msft": data[["Open"]].rename({"Open":"Price"}, axis=1)} 
    timesteps = data.iloc[-5000:].index   

    st = Strategy1()
    bt = BackTester(data_dict, st, 10000)

    bt.run_backtest(timesteps)

    bt.get_results().to_csv("test_results.csv")
    bt.get_strategy_data().to_csv("test_st_data.csv")

