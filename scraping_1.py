import sys
import requests
from multiprocessing import Pool
import asyncio
from timeit import default_timer
from aiohttp import ClientSession
import concurrent.futures
from bs4 import BeautifulSoup
from time import sleep

base_url = 'http://quotes.toscrape.com/page/'

all_urls = list()

NUM_URLS = 500


def generate_urls():
    for i in range(1, NUM_URLS):
        all_urls.append(base_url + str(i))


def scrape(url):
    res = requests.get(url)
    print(res.status_code, res.url)


def async_scrape(urls):
    start_time = default_timer()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(fetch_all(urls))
    loop.run_until_complete(future)
    tot_elapsed = default_timer() - start_time
    print('Total time taken : ' , str(tot_elapsed))


async def fetch_all(urls):
    tasks = []
    fetch.start_time = dict()
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        _ = await asyncio.gather(*tasks)


async def fetch(url, session):
    fetch.start_time[url] = default_timer()
    async with session.get(url) as response:
        r = await response.read()
        elapsed = default_timer() - fetch.start_time[url]
        print(url ,  ' took '  , str(elapsed))
        return r


if __name__ == '__main__':
    generate_urls()
    mode = len(sys.argv)  > 1 and sys.argv[1]
    if mode == "process":
        p = Pool(int(NUM_URLS/10))
        p.map(scrape, all_urls)
        p.terminate()
        p.join()
    elif mode == "thread":
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(NUM_URLS/10)) as executor:
            executor.map(scrape, all_urls)
    elif mode == "async":
        async_scrape(all_urls)
    else:
        for url in all_urls:
            scrape(url)
