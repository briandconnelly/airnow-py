# -*- coding: utf-8 -*-

import argparse
from datetime import date
import os
import sys
from pathlib import Path

import airnow

__DEBUG__ = os.environ.get("AIRNOW_DEBUG", False)


def parse_arguments():
    this_program = Path(sys.argv[0]).name

    parser = argparse.ArgumentParser(
        description="Retrieve air quality information from AirNow",
        epilog=f"To learn more about the commands and their options, see '{this_program} <command> --help'.",
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="format",
        choices=["csv", "json", "pretty", "xml"],
        default="pretty",
        help="Output format",
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

    subparsers = parser.add_subparsers(dest="command", title="commands")

    current_parser = subparsers.add_parser(
        "conditions",
        aliases=[],
        help="Retrieve current air quality conditions for a given location",
        parents=[location_parser],
    )

    forecast_parser = subparsers.add_parser(
        "forecast",
        aliases=[],
        help="Retrieve air quality forecast for a given location",
        parents=[location_parser, date_parser],
    )

    historical_parser = subparsers.add_parser(
        "historical",
        aliases=[],
        help="Retrieve historical air quality observations for a given location",
        parents=[location_parser, date_parser],
    )

    # Show help message and quit if no arguments given
    if len(sys.argv) <= 1:
        parser.print_help()

    args = parser.parse_args()
    return args


def run_cmdline():
    args = parse_arguments()

    if __DEBUG__:
        print("-" * 78)
        print("Command Line Arguments:")
        print(args)
        print("-" * 78)

    if args.command == "conditions":
        if args.zip_code is not None:
            result = airnow.get_conditions_zip(
                zip_code=args.zip_code, distance=args.distance, api_key=args.api_key
            )
            print(result)
        elif args.latitude is not None and args.longitude is not None:
            result = airnow.get_conditions_latlon(
                latitude=args.latitude,
                longitude=args.longitude,
                distance=args.distance,
                api_key=args.api_key,
            )
            print(result)
        else:
            print("Error: must provide either ZIP code or latitude and longitude")
            return 1

    elif args.command == "forecast":
        if args.zip_code is not None:
            result = airnow.get_forecast_zip(
                zip_code=args.zip_code, date=args.date, distance=args.distance, api_key=args.api_key
            )
            print(result)
        elif args.latitude is not None and args.longitude is not None:
            result = airnow.get_forecast_latlon(
                latitude=args.latitude,
                longitude=args.longitude,
                date=args.date,
                distance=args.distance,
                api_key=args.api_key,
            )
            print(result)
        else:
            print("Error: must provide either ZIP code or latitude and longitude")
            return 1

    elif args.command == "historical":
        if args.zip_code is not None:
            result = airnow.get_historical_zip(
                zip_code=args.zip_code, date=args.date, distance=args.distance, api_key=args.api_key
            )
            print(result)
        elif args.latitude is not None and args.longitude is not None:
            result = airnow.get_historical_latlon(
                latitude=args.latitude,
                longitude=args.longitude,
                date=args.date,
                distance=args.distance,
                api_key=args.api_key,
            )
            print(result)
        else:
            print("Error: must provide either ZIP code or latitude and longitude")
            return 1
    else:
        print("Must supply a command")
        return 99


if __name__ == "__main__":
    run_cmdline()
