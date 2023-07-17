import aiohttp
import asyncio
import os
from typing import Any, Dict, List

API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app/'
SALES_ENDPOINT = 'sales'
STATUS_CODE_200 = 200
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")


def unscramble_lists(nested_list: List[Any]) -> List[Any]:
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(unscramble_lists(item))
        else:
            result.append(item)
    return result


# async def fetch_page_data(session: aiohttp.ClientSession,
#                           url: str,
#                           headers: Dict[str, Any],
#                           params: Dict[str, Any],
#                           page: int) -> List[Dict[str, Any]]:
#     print(f"Page {page} started")
#     response = await session.get(url=url, headers=headers, params=params)
#     data = await response.json()
#     print(f"Page {page} done")
#     if response.status == STATUS_CODE_200:
#         return data

async def fetch_page_data(session: aiohttp.ClientSession,
                          url: str,
                          headers: Dict[str, Any],
                          params: Dict[str, Any],
                          page: int) -> List[Dict[str, Any]]:
    response = await session.get(url=url, headers=headers, params=params)
    if response.status == 200:
        print(f"Page {page} started")
        data = await response.json()
        print(f"Page {page} done")
        print('Status_code = 200')
        return data
    else:
        return None


async def get_sales(date: str) -> List[Dict[str, Any]]:
    get_url = os.path.join(API_URL, SALES_ENDPOINT)
    headers = {'Authorization': AUTH_TOKEN}
    params = {'date': date, 'page': 1}
    async with aiohttp.ClientSession() as session:
        results = []
        page = 1
        while True:
            data = await fetch_page_data(session, get_url, headers, params, page)
            if data is None:
                break
            results.append(data)
            page += 1
            params['page'] = page
        gathered_results = unscramble_lists(results)
        gathered_results = [x for x in gathered_results if x is not None]
        return gathered_results
