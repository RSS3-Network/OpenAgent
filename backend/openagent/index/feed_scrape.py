import datetime
import json

import requests

from openagent.conf.env import settings


def fetch_mirror_feeds(since_timestamp, until_timestamp, limit=10) -> dict:
    """
    Fetch feeds from Mirror.
    """
    return fetch_feeds("Mirror", since_timestamp, until_timestamp, limit)


def fetch_iqwiki_feeds(since_timestamp, until_timestamp, limit=10, cursor=None) -> dict:
    """
    Fetch feeds from IQWiki.
    """
    return fetch_feeds("IQ.Wiki", since_timestamp, until_timestamp, limit, cursor)


def fetch_feeds(
    platform, since_timestamp, until_timestamp, limit=10, cursor=None
) -> dict:
    """
    Fetch feeds from a platform.
    """

    cursor_str = f"&cursor={cursor}" if cursor else ""
    url = (
        f"{settings.RSS3_DATA_API}/platforms/{platform}/activities?"
        f"since_timestamp={since_timestamp}&until_timestamp={until_timestamp}&"
        f"limit={limit}{cursor_str}"
    )

    payload = {}  # type: ignore
    headers = {}  # type: ignore

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)


if __name__ == "__main__":
    curr_ts = int(datetime.datetime.now().timestamp())
    _cursor = None
    feeds = fetch_iqwiki_feeds(0, curr_ts, cursor=_cursor)
    print(json.dumps(feeds, indent=4))
