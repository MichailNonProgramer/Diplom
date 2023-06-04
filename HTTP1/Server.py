import asyncio
import random
import ssl
import aiohttp
import aiofiles
from aiohttp import web


async def download_file_mini():
    return await download_file("mini.txt")


async def download_file(filename):
    async with aiofiles.open(filename, 'rb') as f:
        contents = await f.read()
    response = web.Response(body=contents)
    return response


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.options |= ssl.OP_NO_TLSv1  # запрещаем использование TLS 1.0
ssl_context.options |= ssl.OP_NO_TLSv1_1  # запрещаем использование TLS 1.1
ssl_context.set_ciphers(
    'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-CHACHA20-POLY1305')
ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
ssl_context.set_alpn_protocols(['h1'])

semaphore = asyncio.Semaphore(1)


async def download(request):
    print(request.query.get("file"))

    async with semaphore:
        return await download_file('files/' + request.query.get("file"))


async def download_with_lock(request):
    async with semaphore:
        delay = random.randint(5, 10)
        with open(f'download_times_with_holl_locking_timeout.txt', 'a') as f:
            f.write(f'{delay:.3f} seconds\n')
        await asyncio.sleep(delay)
        return await download_file('text.txt')


async def download_with_packet_loss(request):
        # Добавляем искусственную потерю пакетов
        if random.randint(1, 10) == 10:
            return web.Response(status=500)
        return await download(request)


app = web.Application()
app.router.add_get('/download_with_lock', download)
app.router.add_get('/download_with_packet_loss', download_with_packet_loss)

if __name__ == '__main__':
    connector = aiohttp.TCPConnector(ssl=ssl_context)  # включаем использование HTTP/2
    web.run_app(app, port=8443, ssl_context=ssl_context)  # передаем созданный TCPConnector в run_app()
