from abc import ABC, abstractmethod
from typing import Tuple

class StrategyInterface(ABC):

    # Returns list of strategy specific data fields that are calculated by the strategy
    @abstractmethod
    def get_data_fields(self) -> list:
        pass

    @abstractmethod
    def store_ticker_names(self, tickers) -> None:
        pass

    # Takes in current timestep data (multiindex dataframe; index: [ticker, feature]), dict of current stock holdings, and current cash position
    # Returns a tuple of:
        # (dict of new stock holdings, list of calculated values for data fields declared in get_data_fields method)
    @abstractmethod
    def step(self, data, stock, cash) -> Tuple[dict, list]:
        pass

    # Reset all memory variables
    @abstractmethod
    def reset(self):
        pass