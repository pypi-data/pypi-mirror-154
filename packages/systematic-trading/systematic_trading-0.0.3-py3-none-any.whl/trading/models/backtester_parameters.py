"""
Backtester parameters.
"""
from dataclasses import dataclass


# pylint: disable=too-many-instance-attributes
@dataclass
class BacktesterParameters:
    """
    Backtester parameters.
    """

    def __init__(self):
        self.cash = 0
        self.custom = {}
        self.end_date = None
        self.leverage = 1
        self.live = False
        self.no_check = False
        self.plot = True
        self.suffix = ""
        self.start_date = None
        self.tickers = []
