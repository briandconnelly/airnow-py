# -*- coding: utf-8 -*-

import requests


def get_airnow_data(endpoint: str, params: dict, format: str, api_key: str) -> dict:
    """Query the AirNow API and return the contents

    """

    params["format"] = format
    params["API_KEY"] = api_key

    with requests.Session() as s:
        result = requests.get(url=f"http://www.airnowapi.org{endpoint}", params=params)
        return result.content.decode("UTF-8")
