import asyncio
import aiohttp
from aiohttp import ClientSession


async def fetch_page_data(session: ClientSession, url, page: int):
    print(f"Page {page} started")
    response = await session.get(
        url=url,
        params={'date': '2022-08-09', 'page': page},
        headers={'Authorization': '2b8d97ce57d401abd89f45b0079d8790edd940e6'}
    )
    data = await response.json()
    print(f"Page {page} done")
    return data


async def get_sales():
    url = 'https://fake-api-vycpfa6oca-uc.a.run.app/sales'
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(1, 4):
            tasks.append(fetch_page_data(session, url, page))
        results = await asyncio.gather(*tasks)
        return results


res = asyncio.run(get_sales())
print(res)
