from datetime import time
import pandas as pd
import time
import numpy as np

class BackTester:

    # data_dict is a dict of dataframes: {ticker: data}
        # data is a dataframe containing relevant data for the ticker.
            # Must contain at least one column, named Price, with price data 
            # Must be indexed with timesteps (can be either time data or simple integer steps)
    
    # cash is an integer indicating the cash available for the execution of the strategy

    # holdings (optional) is a dict indicating the initial holdings of each ticker
    # If None, 0 stock position for all tickers is assumed.
    def __init__(self, data_dict, strategy, cash, holdings=None):
        
        
        self.strategy = strategy
        self.curr_cash = cash

        self.data = pd.concat(data_dict, names=['ticker'], axis=1) 
        
        self.tickers = data_dict.keys()
        self.strategy.store_ticker_names(list(self.tickers))

        self.curr_holdings = holdings if holdings else {i:0 for i in self.tickers}

        self.results_columns = ["Cash"] + list(self.tickers) + ["Portfolio_Value"]
        self.strategy_data_columns = self.strategy.get_data_fields()

        self.results = dict()
        self.strategy_data = dict()


    # timesteps is an iterable containing the timesteps used to index the data for running the backtest
    def run_backtest(self, timesteps):
        tickers = list(self.tickers)
        for idx in range(len(timesteps) - 1):
            data_row = self.data.loc[timesteps[idx]]
            data_row_next = self.data.loc[timesteps[idx + 1]]
            new_holdings, data_values = self.strategy.step(data_row, self.curr_holdings, self.curr_cash)


            if new_holdings.keys() != self.tickers:
                raise ValueError("Please ensure the strategy returns the same tickers as it was provided!")

            total_cash_change = sum([(new_holdings[i] - self.curr_holdings[i]) * data_row_next[i]['Price'] for i in self.tickers])


            self.curr_holdings = new_holdings
            self.curr_cash = self.curr_cash - total_cash_change

            portfolio_value = sum([self.curr_holdings[i] * data_row_next[i]['Price'] for i in tickers]) + self.curr_cash

            self.results[timesteps[idx]] = [self.curr_cash] + [self.curr_holdings[i] for i in tickers] + [portfolio_value]
            self.strategy_data[timesteps[idx]] = data_values

        


    def get_results(self):
        return pd.DataFrame.from_dict(self.results, orient='index', columns=self.results_columns)

    def get_strategy_data(self):
        return pd.DataFrame.from_dict(self.strategy_data, orient='index', columns=self.strategy_data_columns)
