"""
Market impact access module.
"""
from ..data.constants import FUTURES
from ..utils.contract import ric_to_ticker

DEFAULT_SPREAD = 5e-4


class MarketImpact:
    """
    Market impact.
    """

    def __init__(self):
        pass

    def compute(self):
        """
        Where we will implement the computation of an estimate of the market impact.
        """

    def get(self, ticker=None, ric=None):
        """
        Get the market impact for the instrument.

        Parameters
        ----------
            ticker: str
                Ticker of the instrument.

            ric: str
                RIC of the instrument.

        Returns
        -------
            float
                Market impact for the instrument.
        """
        if ticker is None:
            ticker = ric_to_ticker(ric)
        return FUTURES.get(ticker, {}).get("Spread", DEFAULT_SPREAD)
