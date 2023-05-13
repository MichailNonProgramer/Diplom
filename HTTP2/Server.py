import asyncio
import random
import ssl
from aiohttp import web

async def download_file(request):
    filename = 'text.txt'
    response = web.FileResponse(filename)
    return response

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.options |= ssl.OP_NO_TLSv1  # запрещаем использование TLS 1.0
ssl_context.options |= ssl.OP_NO_TLSv1_1  # запрещаем использование TLS 1.1
ssl_context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-CHACHA20-POLY1305')
ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

semaphore = asyncio.Semaphore(100)

async def download_with_lock(request):
    async with semaphore:
        delay = random.randint(1, 2)
        await asyncio.sleep(delay)
        return await download_file(request)

app = web.Application()
app.router.add_get('/download', download_with_lock)

if __name__ == '__main__':
    web.run_app(app, port=8443, ssl_context=ssl_context)
