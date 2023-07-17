import aiohttp
import asyncio
import os
# from settings import AUTH_TOKEN


print(os.getenv('API_AUTH_TOKEN', 'Нету токена!'))


async def fetch_page_data(session, url, page):
    auth_token = os.getenv('API_AUTH_TOKEN')
    headers = {'Authorization': auth_token} if auth_token else {}
    async with session.get(url, params={'date': '2022-08-09', 'page': page},
                           headers=headers) as response:
        if response.status == 200:
            print(f"Page {page} started")
            data = await response.json()
            print(f"Page {page} done")
            # print(data)
            print('Status_code = 200')
            return data
        else:
            return None

async def get_sales():
    url = 'https://fake-api-vycpfa6oca-uc.a.run.app/sales'
    async with aiohttp.ClientSession() as session:
        results = []
        page = 1
        while True:
            result = await fetch_page_data(session, url, page)
            if result is None:
                break
            results.append(result)
            page += 1
        return results

res = asyncio.run(get_sales())
print(res)