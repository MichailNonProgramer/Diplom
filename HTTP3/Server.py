import asyncio
import os

from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.logger import QuicLogger
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption


class FileTransferProtocol(asyncio.Protocol):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.transport = None
        self.bytes_sent = 0
        self.done = False

    def connection_made(self, transport):
        self.transport = transport
        self.file = open(self.file_path, 'rb')

    def data_received(self, data):
        self.bytes_sent += len(data)
        self.transport.write(data)

    def eof_received(self):
        self.done = True
        return False

    def connection_lost(self, exc):
        if not self.done:
            print(f"Connection lost before transmission was complete: {exc}")
        else:
            print("Transmission complete")
        self.transport.close()
        self.file.close()


async def run_server():
    quic_logger = QuicLogger()
    private_key = load_pem_private_key(
        open(os.path.join(os.path.abspath(os.curdir), "key.pem"), "rb").read(),
        password=None,
    )
    quic_config = QuicConfiguration(is_client=False, quic_logger=quic_logger, private_key=private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()))
    quic_config.load_cert_chain(
        os.path.join(os.path.abspath(os.curdir), "cert.pem"),
        os.path.join(os.path.abspath(os.curdir), "key.pem"),
    )

    protocol_factory = lambda: FileTransferProtocol(file_path="text.txt")
    await serve(
        host='localhost',
        port=4433,
        configuration=quic_config,
        create_protocol=protocol_factory,
    )


if __name__ == "__main__":
    asyncio.run(run_server())
