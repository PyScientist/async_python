import asyncio
import time
import aiohttp


async def download_pep(url: str, session) -> bytes:
    async with session.get(url) as resp:
        content = await resp.read()
        return content


async def write_to_file(pep_number: int, content: bytes):
    file_name = '/'.join(['test_pep', f'async_pep{pep_number}.html'])
    with open(file_name, 'wb') as f:
        f.write(content)


# Since we have two coroutine we can execute it like so:
async def web_scrape_task(pep_number: int, session):
    url = f"https://www.python.org/dev/peps/pep-{pep_number}/"
    downloaded_content = await download_pep(url, session)
    await write_to_file(pep_number, downloaded_content)


async def main():
    connector_app = aiohttp.TCPConnector(ssl=False, limit=100, limit_per_host=25)
    async with aiohttp.ClientSession(connector=connector_app) as session:
        tasks = []
        for i in range(8010, 8016):
            tasks.append(asyncio.create_task(web_scrape_task(i, session)))
            await asyncio.gather(*tasks, return_exceptions=False)


if __name__ == '__main__':
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter()-s
    print(f'Execution time is {elapsed: 0.2f} seconds.')
