# -*- coding: utf-8 -*-

import requests


def get_airnow_data(endpoint: str, **kwargs) -> dict:
    """Query the AirNow API and return the contents

    """

    with requests.Session() as s:
        result = requests.get(url=f"http://www.airnowapi.org{endpoint}", params=kwargs)
        return result.content.decode("UTF-8")
