# airnow

**airnow** is a Python package that provides access to the [AirNow](https://www.airnow.gov) [API](https://docs.airnowapi.org), which reports [air quality](https://docs.airnowapi.org/aq101) data throughout the United States.
To use airnow, you will first need to create an API token by [signing up for an account](https://docs.airnowapi.org/account/request/).


## Installation

You can install airnow by running the following command from this directory:

```sh
pip install .
```

If you'd like to use development mode, install with

```sh
pip install -e .
```

## Usage

Let's get the current air quality conditions for Seattle, Washington (ZIP code 98101):

```py
import airnow

airnow.get_conditions_zip(98102)
```

A dict is returned containing current ozone (O3) and [fine particulate matter](https://en.wikipedia.org/wiki/Particulates#Size,_shape_and_solubility_matter) (PM2.5) readings and associated metadata:

```
[{'DateObserved': '2020-09-21 ',
  'HourObserved': 7,
  'LocalTimeZone': 'PST',
  'ReportingArea': 'Seattle-Bellevue-Kent Valley',
  'StateCode': 'WA',
  'Latitude': 47.562,
  'Longitude': -122.3405,
  'ParameterName': 'O3',
  'AQI': 1,
  'Category': {'Number': 1, 'Name': 'Good'}},
 {'DateObserved': '2020-09-21 ',
  'HourObserved': 7,
  'LocalTimeZone': 'PST',
  'ReportingArea': 'Seattle-Bellevue-Kent Valley',
  'StateCode': 'WA',
  'Latitude': 47.562,
  'Longitude': -122.3405,
  'ParameterName': 'PM2.5',
  'AQI': 40,
  'Category': {'Number': 1, 'Name': 'Good'}}]
```


## Environment Variables

Most airnow functions support reading the API token from the `AIRNOW_API_KEY` environment variable.


## Disclaimer

Neither this package nor its author(s) are affiliated with AirNow or its participating agencies.
Please follow the [U.S. EPA AirNow Data Exchange Guidelines](https://docs.airnowapi.org/docs/DataUseGuidelines.pdf). 
