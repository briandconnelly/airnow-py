# -*- coding: utf-8 -*-

import json
import os

from airnow.api import get_airnow_data


def get_conditions_zip(
    zip_code: str, distance: int = 25, api_key: str = os.environ["AIRNOW_API_KEY"]
) -> dict:
    """
    Get current air quality conditions by ZIP code

    :param str zip_code: A US ZIP code
    :param int distance: If no reporting area exists for given ZIP code, search for nearby stations within this distance (default: 25; unit: miles)
    :param str api_key: AirNow API token

    :return: A dictionary containing the air quality conditions
    """

    params = {
        "zipCode": zip_code,
        "distance": distance,
        "format": "application/json",
        "API_KEY": api_key,
    }

    cond = get_airnow_data(endpoint="/aq/observation/zipCode/current/", **params)
    return json.loads(cond)


def get_conditions_latlon(
    latitude: float,
    longitude: float,
    distance: int = 25,
    api_key: str = os.environ["AIRNOW_API_KEY"],
) -> dict:
    """
    Get current air quality conditions by latitude and longitude

    :param float latitude: Latitude
    :param float longitude: Longitude
    :param int distance: If no reporting area exists for given location, search for nearby stations within this distance (default: 25; unit: miles)
    :param str api_key: AirNow API token

    :return: A dictionary containing the air quality conditions
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "distance": distance,
        "format": "application/json",
        "API_KEY": api_key,
    }

    cond = get_airnow_data(endpoint="/aq/observation/latLong/current/", **params)
    return json.loads(cond)
