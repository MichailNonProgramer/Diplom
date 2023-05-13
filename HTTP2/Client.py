import random

import aiohttp
import asyncio
import os
import ssl
import time
from datetime import datetime

semaphore = asyncio.Semaphore(100)

async def download_file(connector, filename):
    url = 'https://localhost:8443/download'
    if os.path.exists(filename):
        os.remove(filename)
    async with semaphore:
        await asyncio.sleep(random.uniform(2, 3))
        start_time = time.monotonic()
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as response:
                with open(filename, 'wb') as file:
                    async for chunk in response.content.iter_chunked(1024):
                        file.write(chunk)
        end_time = time.monotonic()

    duration = end_time - start_time
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    with open(f'download_times_with_holl_locking.txt', 'a') as f:
        f.write(f'{date_time} - Download took {duration:.3f} seconds\n')


if __name__ == '__main__':
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ssl_context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-CHACHA20-POLY1305')
    ssl_context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3

    loop = asyncio.get_event_loop()
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    NUM_OF_REQUESTS = 100
    filenames = [f'bigfile_downloaded_{i}.txt' for i in range(NUM_OF_REQUESTS)]
    tasks = [loop.create_task(download_file(connector, filename)) for filename in filenames]
    loop.run_until_complete(asyncio.wait(tasks))
