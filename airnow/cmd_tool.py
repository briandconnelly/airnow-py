# -*- coding: utf-8 -*-

import argparse
import logging
import os
import sys

from argparse import ArgumentTypeError
from datetime import date
from pathlib import Path

import dateutil.parser as date_parser

import airnow

logging.basicConfig(
    format="-- [%(asctime)s][%(levelname)s][%(name)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

__DEBUG__ = os.environ.get("AIRNOW_DEBUG", False)

if __DEBUG__:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


def bool_to_int(s: bool) -> int:
    if s:
        return 1
    return 0


def valid_iso_8601(dt_str: str) -> str:
    """Validate date(time) string as ISO 8601 and return datetime object."""

    try:
        dt = date_parser.parse(dt_str)
    except Exception as err:  # noqa: F841
        raise ArgumentTypeError(f"Unable to parse date: {dt_str}")

    if dt.tzinfo:
        raise ArgumentTypeError("Date includes timezone info: {dt_str} - must be UTC")

    return dt.date().isoformat()


def conform_obs_monitoring_args(args):
    """Collect and conform arg options to API compatible syntax."""

    # collect pollutant(s) into comma separated list for `parameters` API input
    pollutants = [
        "o3",
        "pm25",
        "pm10",
        "co",
        "no2",
        "so2",
    ]

    pollutant_parameter = [p for p in pollutants if getattr(args, p)]
    if not pollutant_parameter:
        pollutant_parameter.append("o3")

    args.parameters = ",".join(pollutant_parameter)

    # collect min/max lat-long into comma separated list for `bbox` API input
    bbox_args = ["min_x", "min_y", "max_x", "max_y"]
    args.bbox = ",".join((str(getattr(args, n)) for n in bbox_args))

    # get datatype option (a|b|c)
    datatype = [s for s in "abc" if getattr(args, s)]
    if not datatype:
        datatype = ["b"]

    args.datatype = datatype.pop()

    # convert boolean args to ints
    args.verbose = bool_to_int(args.verbose)
    args.nowcastonly = bool_to_int(args.nowcastonly)
    args.includerawconcentrations = bool_to_int(args.includerawconcentrations)


def construct_obs_monitoring_parser(obs_parser):

    obs_parser.add_argument("min_x", type=float, help="Bounding box minimum latitude")
    obs_parser.add_argument("min_y", type=float, help="Bounding box minimum longitude")
    obs_parser.add_argument("max_y", type=float, help="Bounding box maximum latitude")
    obs_parser.add_argument("max_x", type=float, help="Bounding box maximum longitude")

    obs_parser.add_argument(
        "-s",
        "--start_date",
        dest="startdate",
        type=valid_iso_8601,
        help="UTC start date - isoformat date string",
    )
    obs_parser.add_argument(
        "-e",
        "--end_date",
        dest="enddate",
        type=valid_iso_8601,
        help="UTC end date - isoformat date string",
    )

    obs_parser.add_argument("--o3", action="store_true", help="Parameters - Ozone")
    obs_parser.add_argument("--pm25", action="store_true", help="Parameters - PM2.5")
    obs_parser.add_argument("--pm10", action="store_true", help="Parameters - PM10")
    obs_parser.add_argument("--co", action="store_true", help="Parameters - CO")
    obs_parser.add_argument("--no2", action="store_true", help="Parameters - NO2")
    obs_parser.add_argument("--so2", action="store_true", help="Parameters - SO2")

    # datatype (a,b,c)
    datatype_group = obs_parser.add_mutually_exclusive_group()
    datatype_group.add_argument(
        "-a", "--aqi", dest="a", action="store_true", help="Datatype - enable AQI"
    )
    datatype_group.add_argument(
        "-b",
        "--both_datatypes",
        dest="b",
        action="store_true",
        help="Datatype - enable both AQI & Concentrations",
    )
    datatype_group.add_argument(
        "-c",
        "--concentrations",
        dest="c",
        action="store_true",
        help="Datatype - enable Concentrations",
    )

    # boolean options
    obs_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Provides additional site information including Site Name, Agency Name, AQS ID, and Full AQS ID",
    )
    obs_parser.add_argument(
        "--nowcastonly",
        action="store_true",
        help="Aways provides Nowcast concentrations and AQI regardless of date/tim",
    )
    obs_parser.add_argument(
        "--includerawconcentrations",
        action="store_true",
        help="Include an additional field that contains the raw concentration will be added to the output",
    )


def parse_arguments():
    this_program = Path(sys.argv[0]).name

    parser = argparse.ArgumentParser(
        description="Retrieve air quality information from AirNow",
        epilog=f"To learn more about the commands and their options, see '{this_program} <command> --help'.",
    )

    # params in observation by monitoring site
    parser.set_defaults(parameters=None, bbox=None, datatype=None)

    parser.add_argument(
        "-k",
        "--key",
        dest="API_KEY",
        help="AirNow API token (default: AIRNOW_API_KEY)",
        default=os.environ.get("AIRNOW_API_KEY"),
    )
    parser.add_argument("-v", "--version", action="version", version=airnow.__version__)

    location_parser = argparse.ArgumentParser(add_help=False)
    location_parser.add_argument(
        "-d",
        "--distance",
        dest="distance",
        type=int,
        default=25,
        help="Search distance in miles (default: 25)",
    )
    location_parser.add_argument(
        "-lat", "--latitude", dest="latitude", type=float, help="Target latitude"
    )
    location_parser.add_argument(
        "-lon", "--longitude", dest="longitude", type=float, help="Target longitude"
    )
    location_parser.add_argument(
        "-z", "--zip", dest="zipCode", type=airnow.validation.validate_zip_code, help="Target ZIP code"
    )

    date_parser = argparse.ArgumentParser(add_help=False)
    date_parser.add_argument(
        "-D",
        "--date",
        dest="date",
        type=valid_iso_8601,
        default=date.today().isoformat(),
        help="Target date for forecasts and historical observations (default: today)",
    )

    format_parser = argparse.ArgumentParser(add_help=False)
    format_parser.add_argument(
        "-f",
        "--format",
        dest="format",
        choices=["csv", "json", "xml"],
        default="json",
        help="Output format",
    )

    subparsers = parser.add_subparsers(dest="command", title="commands")

    current_parser = subparsers.add_parser(  # noqa: F841
        "conditions",
        aliases=[],
        help="Retrieve current air quality conditions for a given location",
        parents=[location_parser, format_parser],
    )

    forecast_parser = subparsers.add_parser(  # noqa: F841
        "forecast",
        aliases=[],
        help="Retrieve air quality forecast for a given location",
        parents=[location_parser, date_parser, format_parser],
    )

    historical_parser = subparsers.add_parser(  # noqa: F841
        "historical",
        aliases=[],
        help="Retrieve historical air quality observations for a given location",
        parents=[location_parser, date_parser, format_parser],
    )

    obs_parser = subparsers.add_parser(
        "observations",
        aliases=[],
        help="Retrieve AQI values or data concentrations for a specified date and time range and set of parameters within a geographic area of interest",
        parents=[format_parser],
    )

    construct_obs_monitoring_parser(obs_parser)

    # Show help message and quit if no arguments given
    if len(sys.argv) <= 1:
        parser.print_help()

    args = parser.parse_args()

    if args.command == "observations":
        conform_obs_monitoring_args(args)

    return args


def get_location(args):

    params = {}
    status = True
    loctype = None

    if args.zipCode is not None:
        params["latitude"] = None
        params["longitude"] = None
        loctype = "zipCode"
    elif args.latitude is not None and args.longitude is not None:
        params["zip_code"] = None
        loctype = "latLong"
    else:
        logger.info("Error: must provide either ZIP code or latitude and longitude")
        status = False
    return status, params, loctype


def run_cmdline():

    args = parse_arguments()

    # Quit with error if no command was given
    if args.command is None:
        return 99

    params = vars(args)

    base_api_keys = {"API_KEY", "format"}
    format_mimetypes = {
        "csv": "text/csv",
        "json": "application/json",
        "xml": "application/xml",
    }

    params["format"] = format_mimetypes[params["format"]]

    if __DEBUG__:

        sep = "-" * 78
        msg = ["Command Line Arguments:", args, params]
        for line in msg:
            print(line)
            print(sep)
        print("\n")

    if args.command == "observations":

        cmd_keys = {
            "bbox",
            "startdate",
            "enddate",
            "parameters",
            "datatype",
            "verbose",
            "nowcastonly",
            "includerawconcentrations",
        }

        cmd_params = {k: params[k] for k in base_api_keys if params[k]}
        cmd_params.update({k: params[k] for k in cmd_keys if params[k]})
        cmd_params["unit"] = "ppb"
        cmd_params["startdate"] += "t00"
        cmd_params["enddate"] += "t00"

        result = airnow.api.get_airnow_data(endpoint="/aq/data/", **cmd_params,)
        print(result)
    else:
        status, loc_params, loctype = get_location(args)
        if not status:
            return 1

        params.update(loc_params)

        if args.command == "conditions":
            result = airnow.api.get_airnow_data(
                endpoint="/aq/observation/zipCode/current/", **params,
            )
            print(result)

        elif args.command == "forecast":
            del params["command"]
            params["date"] = args.date

            result = airnow.api.get_airnow_data(
                endpoint=f"/aq/forecast/{loctype}/", **params,
            )
            print(result)

        elif args.command == "historical":
            del params["command"]
            params["date"] = args.date

            result = airnow.api.get_airnow_data(
                endpoint=f"/aq/observation/{loctype}/historical/", **params,
            )
            print(result)


if __name__ == "__main__":
    run_cmdline()
