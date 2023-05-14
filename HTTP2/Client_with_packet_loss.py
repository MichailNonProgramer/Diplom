import random

import aiohttp
import asyncio
import os
import ssl
import time
from datetime import datetime

semaphore = asyncio.Semaphore(100)

async def download_file_with_packet_loss(session, connector, filename):
    url = 'https://localhost:8443/download_with_packet_loss'
    if os.path.exists(filename):
        os.remove(filename)
    while True:
        async with semaphore:
            start_time = time.monotonic()
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise ValueError(f'Response code is {response.status}')
                    with open(filename, 'wb') as file:
                        async for chunk in response.content.iter_chunked(1024):
                            file.write(chunk)
            except Exception as e:
                print(f'Error downloading {filename}: {e}')
                continue
            end_time = time.monotonic()

        duration = end_time - start_time
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        with open(f'download_times_with_packet_loss.txt', 'a') as f:
            f.write(f'{date_time} - Download took {duration:.3f} seconds\n')

        break


async def run_client_with_packet_loss():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ssl_context.set_ciphers(
        'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-CHACHA20-POLY1305')
    ssl_context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
    ssl_context.set_alpn_protocols(['h2'])

    connector = aiohttp.TCPConnector(ssl=ssl_context)
    timeout = aiohttp.ClientTimeout(total=60)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        NUM_OF_REQUESTS = 100
        current_dir = os.getcwd()
        folder_name = 'save'
        new_dir = os.path.join(current_dir, folder_name)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        filenames = [os.path.join(new_dir, f'bigfile_downloaded_{i}.txt') for i in range(NUM_OF_REQUESTS)]
        tasks = [download_file_with_packet_loss(session, connector, filename) for filename in filenames]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(run_client_with_packet_loss())
