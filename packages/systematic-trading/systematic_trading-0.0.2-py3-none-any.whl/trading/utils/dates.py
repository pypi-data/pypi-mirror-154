"""
Date helpers.
"""
from datetime import date


def is_weekend(day: date):
    """
    Say if this day is a weekend or not.

    Parameters
    ----------
        day: date
            Day.

    Returns
    -------
        bool
            True if is weekend.
    """
    return day.weekday() in [5, 6]


def business_days(calendar: list, day: date):
    """
    Returns an integer indicating the xth number day in the month.

    Parameters
    ----------
        calendar: list
            Business days calendar.

        day: date
            Date to be checked.

    Returns
    -------
        int
            xth day in the month.
    """
    first = day.replace(day=1).strftime("%Y-%m-%d")
    days = calendar[calendar >= first]
    return days.get_loc(day) + 1
