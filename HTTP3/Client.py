import asyncio
import os

from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.logger import QuicLogger


class FileReceiverProtocol(asyncio.Protocol):
    def __init__(self, file_path: str, file_size: int):
        self.file_path = file_path
        self.file = None
        self.expected_bytes = file_size
        self.bytes_received = 0

    def connection_made(self, transport):
        self.transport = transport
        self.file = open(self.file_path, 'wb')

    def data_received(self, data):
        self.bytes_received += len(data)
        self.file.write(data)

        if self.bytes_received >= self.expected_bytes:
            self.transport.close()

    def connection_lost(self, exc):
        print("File transfer complete")


async def run_client():
    quic_config = QuicConfiguration(is_client=True)
    server_name = "localhost"
    quic_config.load_verify_locations(os.path.join(os.path.abspath(os.curdir), "cert.pem"))
    quic_logger = QuicLogger()

    async with connect(
            host=server_name,
            port=4433,
            configuration=quic_config,
            logger=quic_logger,
    ) as client:
        reader, writer = await client.create_stream()
        file_size = os.stat("file_to_receive.txt").st_size

        # send file size to server
        writer.write(str(file_size).encode())
        await writer.drain()

        # wait for response from the server
        data = await reader.read(1024)
        if not data:
            print("No response received from server")
        else:
            # start receiving file
            receiver = FileReceiverProtocol("file_to_receive.txt", file_size)
            await client.create_stream().send_all(data)
            await client.create_stream(receiver).recv()


if __name__ == "__main__":
    asyncio.run(run_client())
