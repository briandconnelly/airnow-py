# -*- coding: utf-8 -*-

import json
import os

from airnow.api import get_airnow_data


def get_historical_zip(
    zip_code: int,
    date: str,
    distance: int = 25,
    api_key: str = os.environ["AIRNOW_API_KEY"],
) -> dict:
    """
    Get historical air quality conditions for a given date by ZIP code

    :param int zip_code: A US ZIP code
    :param str date: Date from which to get the forecast (default: today)
    :param int distance: If no reporting area exists for given ZIP code, search for nearby stations within this distance (default: 25; unit: miles)
    :param str api_key: AirNow API token

    :return: A dictionary containing the air quality conditions
    """

    params = {
        "zipCode": zip_code,
        "date": f"{date}T00-0000",
        "distance": distance,
        "format": "application/json",
        "API_KEY": api_key,
    }

    cond = get_airnow_data(
        endpoint="/aq/observation/zipCode/historical/", params=params,
    )
    return json.loads(cond)


def get_historical_latlon(
    latitude: float,
    longitude: float,
    date: str,
    distance: int = 25,
    api_key: str = os.environ["AIRNOW_API_KEY"],
) -> dict:
    """
    Get historical air quality conditions for a given date by latitude and longitude

    :param float latitude: Latitude
    :param float longitude: Longitude
    :param str date: Date from which to get the forecast (default: today)
    :param int distance: If no reporting area exists for given location, search for nearby stations within this distance (default: 25; unit: miles)
    :param str api_key: AirNow API token

    :return: A dictionary containing the air quality conditions
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "date": f"{date}T00-0000",
        "distance": distance,
        "format": "application/json",
        "API_KEY": api_key,
    }

    cond = get_airnow_data(
        endpoint="/aq/observation/latLong/historical/", params=params,
    )
    return json.loads(cond)
