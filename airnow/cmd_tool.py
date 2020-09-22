# -*- coding: utf-8 -*-

import argparse
import logging
import os
import sys

from datetime import date
from pathlib import Path

import airnow

logging.basicConfig(
    format="-- [%(asctime)s][%(levelname)s][%(name)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

__DEBUG__ = os.environ.get("AIRNOW_DEBUG", True)

if __DEBUG__:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

format_mimetypes = {
    "csv": "text/csv",
    "json": "application/json",
    "xml": "application/xml",
}


def parse_arguments():
    this_program = Path(sys.argv[0]).name

    parser = argparse.ArgumentParser(
        description="Retrieve air quality information from AirNow",
        epilog=f"To learn more about the commands and their options, see '{this_program} <command> --help'.",
    )
    parser.add_argument(
        "-k",
        "--key",
        dest="api_key",
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
        "-z", "--zip", dest="zip_code", type=int, help="Target ZIP code"
    )

    date_parser = argparse.ArgumentParser(add_help=False)
    date_parser.add_argument(
        "-D",
        "--date",
        dest="date",
        type=str,
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

    current_parser = subparsers.add_parser(
        "conditions",
        aliases=[],
        help="Retrieve current air quality conditions for a given location",
        parents=[location_parser, format_parser],
    )

    forecast_parser = subparsers.add_parser(
        "forecast",
        aliases=[],
        help="Retrieve air quality forecast for a given location",
        parents=[location_parser, date_parser, format_parser],
    )

    historical_parser = subparsers.add_parser(
        "historical",
        aliases=[],
        help="Retrieve historical air quality observations for a given location",
        parents=[location_parser, date_parser, format_parser],
    )

    # Show help message and quit if no arguments given
    if len(sys.argv) <= 1:
        parser.print_help()

    args = parser.parse_args()
    return args


def get_location(args):

    params = {}
    status = True
    loctype = None

    if args.zip_code is not None:
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

    params = {
        "zipCode": args.zip_code,
        "latitude": args.latitude,
        "longitude": args.longitude,
        "distance": args.distance,
    }

    if __DEBUG__:
        print("-" * 78)
        print("Command Line Arguments:")
        print(args)
        print("-" * 78)
        print("\n")

    status, loc_params, loctype = get_location(args)
    if not status:
        return 1

    params.update(loc_params)

    if args.command == "conditions":
        result = airnow.api.get_airnow_data(
            endpoint="/aq/observation/zipCode/current/",
            params=params,
            format=format_mimetypes[args.format],
            api_key=args.api_key,
        )
        print(result)

    elif args.command == "forecast":
        params["date"] = args.date
        result = airnow.api.get_airnow_data(
            endpoint=f"/aq/forecast/{loctype}/",
            params=params,
            format=format_mimetypes[args.format],
            api_key=args.api_key,
        )
        print(result)

    elif args.command == "historical":
        params["date"] = args.date
        result = airnow.api.get_airnow_data(
            endpoint="/aq/observation/{loctype}/historical/",
            params=params,
            format=format_mimetypes[args.format],
            api_key=args.api_key,
        )
        print(result)

    else:
        return 99


if __name__ == "__main__":
    run_cmdline()
