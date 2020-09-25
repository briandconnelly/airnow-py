# -*- coding: utf-8 -*-

import pytest

from datetime import datetime
from airnow import validation


@pytest.mark.parametrize("x", ["01234", "98109"])
def test__validate_zip_code(x):
    assert validation.validate_zip_code(x) == x


@pytest.mark.parametrize("x", ["", "0123", "666666"])
def test__validate_zip_code__value_exception(x):
    with pytest.raises(ValueError):
        validation.validate_zip_code(x)


@pytest.mark.parametrize("x", [None, 98109])
def test__validate_zip_code__type_exception(x):
    with pytest.raises(TypeError):
        validation.validate_zip_code(x)


@pytest.mark.parametrize(
    "dt_str, expected",
    [
        ("2020-09-01", datetime(2020, 9, 1)),
        ("2020-09-01T12:00:00", datetime(2020, 9, 1, 12)),
    ],
)
def test__validate_iso_8601(dt_str, expected):
    assert validation.validate_iso_8601(dt_str) == expected


@pytest.mark.parametrize("dt_str", ["2020-09-01T00:00:00+00:00"])
def test__validate_iso_8601__tz_exception(dt_str):
    with pytest.raises(ValueError):
        validation.validate_iso_8601(dt_str)


@pytest.mark.parametrize("dt_str", ["202009"])
def test__validate_iso_8601__parse_exception(dt_str):
    with pytest.raises(ValueError):
        validation.validate_iso_8601(dt_str)


@pytest.mark.parametrize("n", [0, -90, 90])
def test__validate_latitude(n):
    assert validation.validate_latitude(n) == n


@pytest.mark.parametrize("n", [0, -180, 180])
def test__validate_longitude(n):
    assert validation.validate_longitude(n) == n
