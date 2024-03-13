import asyncio

import aiohttp
from aiocache import Cache
from aiocache.decorators import cached
from loguru import logger


def get_token_data_by_key(token, key) -> str:
    return token[key] if (token and key in token) else ""


@cached(ttl=60, cache=Cache.MEMORY)
async def cached_get():
    logger.info("Attempting to retrieve data for https://li.quest/v1/tokens")

    url = """https://li.quest/v1/tokens"""
    headers = {"Accept": "application/json"}
    logger.info(f"Fetching new data from {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            token_list = await response.json()
            eth_list = token_list["tokens"]["1"]
            return eth_list


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
            return results[0]

        # Sorting based on priority
        results.sort(
            key=lambda x: (x["address"].lower() == address,),
            reverse=True,
        )
        return results[0]
    raise Exception("Token not found")


async def select_best_token(keyword) -> dict | None:
    keyword = handle_token(keyword)
    ct_token = handle_ct_token(keyword)
    if ct_token:
        return ct_token
    tokens = await cached_get()
    # Filtering based on symbol and name
    results = [
        token
        for token in tokens
        if token["symbol"].lower() == keyword
        or token["name"].lower() == keyword
        or token["coinKey"].lower() == keyword
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
    if addr in ["0x4d2bf3A34a2311dB4b3D20D4719209EDaDBf69b6"]:
        return {
            "address": "0x4d2bf3A34a2311dB4b3D20D4719209EDaDBf69b6",
            "symbol": "CT",
            "decimals": 6,
            "coinKey": "ct",
            "chainId": 1,
        }
    return None


async def main():
    token = await get_token_by_address("0x4d2bf3A34a2311dB4b3D20D4719209EDaDBf69b6")
    best_token = await select_best_token("ct")
    print(best_token)
    print(token)


if __name__ == "__main__":
    asyncio.run(main())
