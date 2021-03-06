# -*- coding: utf-8 -*-

from datetime import date
import json
import os

from airnow.api import get_airnow_data


def get_forecast_zip(
    zip_code: str,
    date: str = date.today().isoformat(),
    distance: int = 25,
    api_key: str = os.environ["AIRNOW_API_KEY"],
) -> dict:
    """
    Get air quality forecast by ZIP code

    :param str zip_code: A US ZIP code
    :param str date: Date from which to get the forecast (default: today)
    :param int distance: If no reporting area exists for given ZIP code, search for nearby stations within this distance (default: 25; unit: miles)
    :param str api_key: AirNow API token

    :return: A dictionary containing the air quality forecast
    """

    params = {
        "zipCode": zip_code,
        "date": date,
        "distance": distance,
        "format": "application/json",
        "API_KEY": api_key,
    }

    forecast = get_airnow_data(endpoint="/aq/forecast/zipCode/", **params)
    return json.loads(forecast)


def get_forecast_latlon(
    latitude: float,
    longitude: float,
    date: str = date.today().isoformat(),
    distance: int = 25,
    api_key: str = os.environ["AIRNOW_API_KEY"],
) -> dict:
    """
    Get air quality forecast by latitude and longitude

    :param float latitude: Latitude
    :param float longitude: Longitude
    :param str date: Date from which to get the forecast (default: today)
    :param int distance: If no reporting area exists for given location, search for nearby stations within this distance (default: 25; unit: miles)
    :param str api_key: AirNow API token

    :return: A dictionary containing the air quality forecast
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "date": date,
        "distance": distance,
        "format": "application/json",
        "API_KEY": api_key,
    }

    forecast = get_airnow_data(endpoint="/aq/forecast/latLong/", **params)
    return json.loads(forecast)
