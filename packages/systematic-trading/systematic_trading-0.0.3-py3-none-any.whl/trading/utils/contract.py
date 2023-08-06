"""
Contract management functions.
"""
from datetime import date, datetime, timedelta

import ring

from ..data.client import Client
from ..data.constants import FUTURES, START_DATE


client = Client()


def format_ric_if_is_active_or_not(ric):
    """
    Says if a RIC is still active or not and converts it if needed.

    Parameters
    ----------
        ric: str
            RIC of the contract.

    Returns
    -------
        str
            RIC.

        bool
            True if this is a recent RIC.
    """
    is_recent_ric = False
    if "^" in ric:
        year_3 = ric.split("^")[1]
        year_4 = ric.split("^")[0][-1]
        year_12 = "19" if year_3 in ["8", "9"] else "20"
        year = int(f"{year_12}{year_3}{year_4}")
        is_recent_ric = year >= (date.today() - timedelta(days=365)).year
        if is_recent_ric and not ric_exists(ric):
            ric = ric.split("^")[0]
    return ric, is_recent_ric


@ring.lru()
def get_contract(ticker: str, day: date, contract_rank: int = 0):
    """
    Get the contract characteristics.

    Parameters
    ----------
        ticker: str
            Ticker of the contract.

        day: date
            Date of the contract to be checked.

        contract_rank: int
            Ranke of the contract. 0 is the front contract.

    Returns
    -------
        date
            Last trading date.

        str
            RIC.
    """
    chain = get_chain(ticker, day)
    contract = chain.iloc[contract_rank, :]
    ltd = datetime.strptime(contract.LTD, "%Y-%m-%d").date()
    ric = contract.RIC
    ric, _ = format_ric_if_is_active_or_not(ric)
    return ltd, ric


def get_front_contract(day: date, ticker: str):
    """
    Get the front contract characteristics.

    Parameters
    ----------
        ticker: str
            Ticker of the contract.

        day: date
            Date of the contract to be checked.

    Returns
    -------
        date
            Last trading date.

        str
            RIC.
    """
    future = FUTURES.get(ticker, {})
    roll_offset_from_reference = timedelta(
        days=future.get("RollOffsetFromReference", -31)
    )
    reference_day = day - roll_offset_from_reference
    return get_contract(ticker=ticker, day=reference_day, contract_rank=0)


def get_next_contract(day: date, ticker: str):
    """
    Get the next contract characteristics.

    Parameters
    ----------
        ticker: str
            Ticker of the contract.

        day: date
            Date of the contract to be checked.

    Returns
    -------
        date
            Last trading date.

        str
            RIC.
    """
    future = FUTURES.get(ticker, {})
    roll_offset_from_reference = timedelta(
        days=future.get("RollOffsetFromReference", -31)
    )
    reference_day = day - roll_offset_from_reference
    return get_contract(ticker=ticker, day=reference_day, contract_rank=1)


@ring.lru()
def ric_to_ticker(ric: str):
    """
    Convert a RIC to a ticker.

    Parameters
    ----------
        ric: str
            RIC of the contract.

    Returns
    -------
        str
            Ticker.
    """
    suffix = "^"
    stem_wo_suffix = ric.split(suffix)[0] if suffix in ric else ric
    delayed_data_prefix = "/"
    stem_wo_prefix = (
        stem_wo_suffix.split(delayed_data_prefix)[-1]
        if delayed_data_prefix in stem_wo_suffix
        else stem_wo_suffix
    )
    stem_wo_year = "".join([c for c in stem_wo_prefix if not c.isdigit()])
    stem_wo_month = stem_wo_year[:-1]
    if stem_wo_month in ["SIRT"]:
        return "SI"
    for ticker in FUTURES.keys():
        if stem_wo_month == FUTURES[ticker].get("Stem", {}).get("Reuters"):
            return ticker
    return None


@ring.lru()
def stem_to_ric(contract_rank: int, day: date, stem: str):
    """
    Get the contract characteristics.

    Parameters
    ----------
        contract_rank: int
            Ranke of the contract. 0 is the front contract.

        day: date
            Date of the contract to be checked.

        stem: str
            Stem of the contract.

    Returns
    -------
        str
            RIC.
    """
    chain = get_chain(stem, day)
    contract = chain.iloc[contract_rank, :]
    return contract.RIC


@ring.lru()
def get_first_trade_date(ric: str):
    """
    Get the contract first trade date.

    Parameters
    ----------
        ric: str
            RIC of the contract.

    Returns
    -------
        date
            First trade date.
    """
    ticker = ric_to_ticker(ric)
    chain = get_chain(ticker=ticker)
    if "^" in ric:
        contracts = chain.loc[chain.RIC == ric, "FTD"]
        if contracts.shape[0] == 0:
            return None
        first_trade_date = datetime.strptime(contracts.iloc[0], "%Y-%m-%d").date()
    else:
        index = chain.RIC.apply(lambda x: x.split("^")[0]) == ric
        contracts = chain.loc[index, :]
        if contracts.shape[0] == 0:
            return None
        ltd = min(
            contracts.LTD,
            key=lambda x: abs(datetime.strptime(x, "%Y-%m-%d").date() - date.today()),
        )
        ftd = contracts.FTD[contracts.LTD == ltd].iloc[0]
        first_trade_date = datetime.strptime(ftd, "%Y-%m-%d").date()
    return first_trade_date


@ring.lru()
def get_last_trade_date(ric: str):
    """
    Get the contract last trade date.

    Parameters
    ----------
        ric: str
            RIC of the contract.

    Returns
    -------
        date
            Last trade date.
    """
    ticker = ric_to_ticker(ric)
    chain = get_chain(ticker=ticker)
    if "^" in ric:
        contracts = chain.loc[chain.RIC == ric, "LTD"]
        if contracts.shape[0] == 0:
            return None
        last_trade_date = datetime.strptime(contracts.iloc[0], "%Y-%m-%d").date()
    else:
        index = chain.RIC.apply(lambda x: x.split("^")[0]) == ric
        contracts = chain.loc[index, :]
        if contracts.shape[0] == 0:
            return None
        ltd = min(
            contracts.LTD,
            key=lambda x: abs(datetime.strptime(x, "%Y-%m-%d").date() - date.today()),
        )
        last_trade_date = datetime.strptime(ltd, "%Y-%m-%d").date()
    return last_trade_date


@ring.lru()
def get_expiry_calendar(ticker: str):
    """
    Get the expiry calendar.

    Parameters
    ----------
        ticker: str
            Ticker of the contract.

    Returns
    -------
        DataFrame
            Expiry calendar.
    """
    dfm, _ = client.get_expiry_calendar(ticker)
    return dfm


@ring.lru()
def get_chain(ticker: str, day: date = START_DATE, minimum_time_to_expiry: int = 0):
    """
    Get the future contract chain for a given ticker, day and minimum time to expiry.

    Parameters
    ----------
        ticker: str
            Ticker of the contract.

        day: date
            Day of the contract

        minimum_time_to_expiry: int
            Minimum time to expiry.

    Returns
    -------
        DataFrame
            Contract chain.
    """
    dfm = get_expiry_calendar(ticker)
    if datetime.strptime(dfm.LTD.iloc[-1], "%Y-%m-%d").date() - day < timedelta(
        days=minimum_time_to_expiry
    ):
        expiry_calendar = FUTURES.get(ticker, {}).get("ExpiryCalendar", "")
        raise Exception(
            f"Not enough data for {ticker}. Download expiry data from {expiry_calendar}"
        )
    index = (dfm.LTD >= day.isoformat()) & (dfm.WeTrd == 1)  # pylint: disable=no-member
    return dfm.loc[index, :].reset_index(drop=True)  # pylint: disable=no-member


@ring.lru()
def ric_exists(ric: str):
    """
    Check is the RIC exists.

    Parameters
    ----------
        ric: str
            RIC of the contract.

    Returns
    -------
        bool
            True if the RIC exists.
    """
    data, _ = client.get_health_ric(ric)
    return data


@ring.lru()
def will_expire_soon(ric: str, day: date = date.today()):
    """
    Get the future contract chain for a given ticker, day and minimum time to expiry.

    Parameters
    ----------
        ric: str
            RIC of the contract.

        day: date
            Day of the contract

    Returns
    -------
        bool
            True if the contract expires soon. False otherwise.
    """
    last_trade_date = get_last_trade_date(ric)
    return day > last_trade_date - timedelta(days=10)


def stem_to_ticker(stem: str):
    """
    Convert a stem to a ticker.

    Parameters
    ----------
        stem: str
            Stem of the contract.

    Returns
    -------
        str
            Ticker.
    """
    tickers = [
        k for k, v in FUTURES.items() if v.get("Stem", {}).get("Reuters") == stem
    ]
    if len(tickers) != 1:
        raise Exception(
            f"No future with Stem.Reuters {stem}. Double check file database-futures.json"
        )
    ticker = tickers[0]

    return ticker
