import os
import sys
import json
import argparse
import logging

import requests
import tweepy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_location(q):
    if not q:
        return

    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={
            "q": q,
            "format": "json",
        },
    )
    data = response.json()

    if len(data) > 0:
        return data[0]

    logger.warning(f"Couldn't find location for: {q}")


def main(args):
    keys = {
        key: os.getenv(key)
        for key in (
            "TWITTER_API_KEY",
            "TWITTER_API_SECRET",
            "TWITTER_TOKEN_KEY",
            "TWITTER_TOKEN_SECRET",
        )
    }

    if missing := [key for key, value in keys.items() if not value]:
        sys.exit(f"Missing env variables: {missing}")

    stream = tweepy.Stream(*keys.values())
    filters = {}

    if location := get_location(args.location):
        slat, nlat, wlon, elon = (float(coord) for coord in location["boundingbox"])
        print("+ Location: ", location["display_name"], file=sys.stderr)
        print(
            "+ Map:",
            f"https://openstreetmap.org/relation/{location['osm_id']} / http://bboxfinder.com/#{slat},{wlon},{nlat},{elon}",
            file=sys.stderr,
        )
        filters["locations"] = (wlon, slat, elon, nlat)

    if args.query:
        filters["track"] = args.query.split(",")

    if not filters:
        sys.exit("No filters")

    print("+ Filters: ", filters, file=sys.stderr)

    def on_status(status):
        if args.json:
            json.dump(status._json, sys.stdout)
        else:
            print(
                f"@{status.user.screen_name}: ",
                status.text,
                f"... https://twitter.com/user/status/{status.id_str}" if "https://t.co" not in status.text else "",
                flush=True,
            )

    try:
        stream.on_status = on_status
        stream.filter(**filters)
    except KeyboardInterrupt:
        pass
    finally:
        stream.disconnect()


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="filter keywords separated by comma")
    parser.add_argument("-l", "--location", help="location string, geocoded by openstreemap's nominatim")
    parser.add_argument("-j", "--json", action="store_true", default=False, help="output json")
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli()
