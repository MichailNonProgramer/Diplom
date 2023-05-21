import random

import aiohttp
import asyncio
import os
import ssl
import time
from datetime import datetime

semaphore = asyncio.Semaphore(1)

async def download(session, filename):
    url = 'https://localhost:8443/download'
    async with session.get(url) as response:
        with open(filename, 'wb') as file:
            async for chunk in response.content.iter_chunked(1024):
                file.write(chunk)

async def download_file(session, filename):
    url = 'https://localhost:8443/download_with_packet_loss'
    if os.path.exists(filename):
        os.remove(filename)
    async with semaphore:
        start_time = time.monotonic()
        try:
            async with session.get(url) as response:
                with open(filename, 'wb') as file:
                    async for chunk in response.content.iter_chunked(1024):
                        file.write(chunk)
        except Exception:
            await download(session, filename)
        end_time = time.monotonic()

    duration = end_time - start_time
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    with open(f'download_with_lock_дщслштп.txt', 'a') as f:
        f.write(f'{date_time} - Download took {duration:.3f} seconds\n')

async def run_client():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ssl_context.set_ciphers(
        'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-CHACHA20-POLY1305')
    ssl_context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
    ssl_context.set_alpn_protocols(['h1'])

    connector = aiohttp.TCPConnector(ssl=ssl_context)
    timeout = aiohttp.ClientTimeout(total=60)
    all_time = time.monotonic()
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        NUM_OF_REQUESTS = 100
        current_dir = os.getcwd()
        folder_name = 'save'
        new_dir = os.path.join(current_dir, folder_name)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        filenames = [os.path.join(new_dir, f'bigfile_downloaded_{i}.txt') for i in range(NUM_OF_REQUESTS)]
        tasks = [download_file(session, filename) for filename in filenames]
        await asyncio.gather(*tasks)
        end_timeAllTime = time.monotonic()
        duration = end_timeAllTime - all_time
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        with open(f'AllTimeFile.txt', 'a') as f:
            f.write(f'{date_time} - download_with_packet_loss {duration:.3f} seconds\n')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run_client())
