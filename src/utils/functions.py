import pandas as pd

from re import sub
from decimal import Decimal


def parse_value(value: str) -> int:
    return Decimal(sub(r"[^\d\-.]", "", value))


def parse_str_value(dataframe: pd.DataFrame, target: str) -> list:
    values = list(dataframe[target])
    return [parse_value(value) for value in values]
