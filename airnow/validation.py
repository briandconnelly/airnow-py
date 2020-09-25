# -*- coding: utf-8 -*-

import datetime
import dateutil.parser as date_parser
import re

from typing import Union


def validate_zip_code(x):
    """Test whether a given value is a valid 5-decimal US ZIP code."""
    if not isinstance(x, str):
        raise TypeError("Value should be a string")

    zip_pattern = re.compile(r"^\d{5}$")

    if not zip_pattern.match(x):
        raise ValueError(f"{x} is not a valid 5-decimal US ZIP code (e.g., '02133')")

    return x


def validate_iso_8601(dt_str: str) -> datetime.datetime:
    """Validate date(time) string as ISO 8601 and return datetime object."""

    try:
        dt = date_parser.parse(dt_str)
    except Exception as err:  # noqa: F841
        raise ValueError(f"Unable to parse date: {dt_str}")

    if dt.tzinfo:
        raise ValueError("Date includes timezone info: {dt_str} - must be UTC")

    return dt


def validate_latitude(n: Union[str, float]) -> float:

    if isinstance(n, str):
        n = float(n)

    if abs(n) > 90:
        raise ValueError()
    return n


def validate_longitude(n: Union[str, float]) -> float:

    if isinstance(n, str):
        n = float(n)

    if abs(n) > 180:
        raise ValueError()
    return n
