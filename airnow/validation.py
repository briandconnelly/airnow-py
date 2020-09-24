# -*- coding: utf-8 -*-

import re


def validate_zip_code(x):
    """Test whether a given value is a valid 5-decimal US ZIP code."""
    if not isinstance(x, str):
        raise TypeError("Value should be a string")

    zip_pattern = re.compile("^\d{5}$")

    if not zip_pattern.match(x):
        raise ValueError(f"{x} is not a valid 5-decimal US ZIP code (e.g., '02133')")

    return x
