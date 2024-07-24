import json

import requests
from loguru import logger
from retrying import retry

from openagent.conf.env import settings


def fetch_mirror_feeds(since_timestamp, until_timestamp, limit=10, cursor=None) -> dict:
    """
    Fetch feeds from Mirror.
    """
    return fetch_feeds("Mirror", since_timestamp, until_timestamp, limit, cursor)


def fetch_iqwiki_feeds(since_timestamp, until_timestamp, limit=10, cursor=None) -> dict:
    """
    Fetch feeds from IQWiki.
    """
    return fetch_feeds("IQ.Wiki", since_timestamp, until_timestamp, limit, cursor)


def fetch_feeds(platform, since_timestamp, until_timestamp, limit=10, cursor=None, max_retries=3) -> dict:
    """
    Fetch feeds from a platform with retry functionality.
    """

    @retry(stop_max_attempt_number=max_retries)
    def _fetch_feeds():
        cursor_str = f"&cursor={cursor}" if cursor else ""
        url = (
            f"{settings.RSS3_DATA_API}/decentralized/platform/{platform}?limit={limit}"
            f"&action_limit=10&since_timestamp={since_timestamp}&type=post&"
            f"until_timestamp={until_timestamp}{cursor_str}"
        )
        payload = {}  # type: ignore
        headers = {}  # type: ignore

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch feeds: {response.text}")

        return json.loads(response.text)

    try:
        return _fetch_feeds()
    except Exception as e:
        logger.error(f"Failed to fetch feeds from {platform}: {e}")
        return {}


if __name__ == "__main__":
    feeds = fetch_feeds("Mirror", 0, 0, 1, None, 3)
    print(json.dumps(feeds, ensure_ascii=False))
