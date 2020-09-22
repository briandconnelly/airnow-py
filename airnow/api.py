# -*- coding: utf-8 -*-

import requests


def get_airnow_data(endpoint: str, **kwargs) -> dict:
    """Query the AirNow API and return the contents

    :param str endpoint: AirNow API endpoint (e.g., "/aq/observation/zipCode/current")

    Additional named arguments are passed on as query parameters.
    All queries should at least have `API_KEY` set.
    See the AirNow API documentation for parameter lists and descriptions.
    """

    with requests.Session() as s:
        result = requests.get(url=f"http://www.airnowapi.org{endpoint}", params=kwargs)
        return result.content.decode("UTF-8")
