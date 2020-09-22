# -*- coding: utf-8 -*-

import os

import requests


def get_airnow_data(endpoint: str, params: dict) -> dict:
    """Query the AirNow API and return the contents

    """

    with requests.Session() as s:
        result = requests.get(url=f"http://www.airnowapi.org{endpoint}", params=params)
        return result.content.decode("UTF-8")
