"""
Definition of the constants of the module
"""
from datetime import date
import json
import os


EMPTY = "empty"
LAST_MODIFIED = "last-modified"

script_path = os.path.abspath(os.path.dirname(__file__))
with open(
    os.path.join(script_path, "database-futures.json"), "r", encoding="utf-8"
) as handler:
    FUTURES = json.load(handler)

FUTURE_TYPE = "Future"

LETTERS = ["F", "G", "H", "J", "K", "M", "N", "Q", "U", "V", "X", "Z"]

LIBOR_BEFORE_2001 = 6.65125

START_DATE = date(2000, 1, 1)
