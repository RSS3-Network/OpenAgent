import asyncio

import aiohttp
from aiocache import Cache
from aiocache.decorators import cached
from loguru import logger


def get_token_data_by_key(token, key) -> str:
    return str(token[key]) if (token and key in token) else ""


def chain_name_to_id(chain_name: str) -> str:
    chain_name = chain_name.lower()
    chain_map = {
        "ethereum": "1",
        "optimism": "10",
        "binance_smart_chain": "56",
        "polygon": "137",
        "arbitrum": "42161",
    }
    return chain_map.get(chain_name, "1")


@cached(ttl=60, cache=Cache.MEMORY)
async def cached_get(chain_id: str):
    logger.info("Attempting to retrieve data for https://li.quest/v1/tokens")

    url = """https://li.quest/v1/tokens"""
    headers = {"Accept": "application/json"}
    logger.info(f"Fetching new data from {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            token_list = await response.json()
            token_list_on_chain = token_list["tokens"][chain_id]
            return token_list_on_chain


def handle_token(token: str) -> str:
    token = token.lower()
    token = handle_special_case(token)
    return token


def handle_special_case(token: str) -> str:
    special_cases = {
        "btc": "wbtc",
    }
    if token in special_cases:
        return special_cases[token]
    return token


async def get_token_by_address(address: str) -> dict:
    ct_token = handle_ct_token_by_address(address)
    if ct_token:
        return ct_token
    tokens = await cached_get()
    # Filtering based on symbol and name
    results = [token for token in tokens if token["address"].lower() == address]

    if results:
        if len(results) == 1:
            return dict(results[0])

        # Sorting based on priority
        results.sort(
            key=lambda x: (x["address"].lower() == address,),
            reverse=True,
        )
        return dict(results[0])
    raise Exception("Token not found")


async def select_best_token(keyword, chain_id) -> dict | None:
    keyword = handle_token(keyword)
    ct_token = handle_ct_token(keyword)
    if ct_token:
        return ct_token
    tokens = await cached_get(chain_id)
    # Filtering based on symbol and name
    try:
        results = [
            token
            for token in tokens
            if token["symbol"].lower() == keyword
            or token["name"].lower() == keyword
            or token["coinKey"].lower() == keyword
        ]
    except Exception:
        pass
    finally:
        results = [
            token
            for token in tokens
            if token["symbol"].lower() == keyword or token["name"].lower() == keyword
        ]

    if results:
        if len(results) == 1:
            return results[0]

        # Sorting based on priority
        results.sort(
            key=lambda x: (
                x["symbol"].lower() == keyword,
                x["coinKey"].lower() == keyword,
                x["name"].lower() == keyword,
            ),
            reverse=True,
        )
        return results[0]
    return None


def handle_ct_token(kw) -> dict | None:
    if kw in ["ct", "copilot token"]:
        return {
            "address": "0x4d2bf3A34a2311dB4b3D20D4719209EDaDBf69b6",
            "symbol": "CT",
            "decimals": 6,
            "coinKey": "ct",
            "chainId": 1,
        }
    return None


def handle_ct_token_by_address(addr) -> dict | None:
    if addr == "0x4d2bf3A34a2311dB4b3D20D4719209EDaDBf69b6":
        return {
            "address": "0x4d2bf3A34a2311dB4b3D20D4719209EDaDBf69b6",
            "symbol": "CT",
            "decimals": 6,
            "coinKey": "ct",
            "chainId": 1,
        }
    return None
