import asyncio
import ipaddress
import socket
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable, Optional, cast
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from ..QUIC.config import QuicConfiguration
from ..QUIC.connection import QuicConnection
from ..tls import SessionTicketHandler
from .protocol import QuicConnectionProtocol, QuicStreamHandler

__all__ = ["connect"]


if not hasattr(socket, "IPPROTO_IPV6"):
    socket.IPPROTO_IPV6 = 41


@asynccontextmanager
async def connect(
    host: str,
    port: int,
    *,
    configuration: Optional[QuicConfiguration] = None,
    create_protocol: Optional[Callable] = QuicConnectionProtocol,
    session_ticket_handler: Optional[SessionTicketHandler] = None,
    stream_handler: Optional[QuicStreamHandler] = None,
    wait_connected: bool = True,
    local_port: int = 0,
) -> AsyncGenerator[QuicConnectionProtocol, None]:

    loop = asyncio.get_event_loop()
    local_host = "::"


    try:
        ipaddress.ip_address(host)
        server_name = None
    except ValueError:
        server_name = host

    # lookup remote address
    infos = await loop.getaddrinfo(host, port, type=socket.SOCK_DGRAM)
    addr = infos[0][4]
    if len(addr) == 2:
        addr = ("::ffff:" + addr[0], addr[1], 0, 0)

    # prepare QUIC connection
    if configuration is None:
        configuration = QuicConfiguration(is_client=True)
    if configuration.server_name is None:
        configuration.server_name = server_name
    connection = QuicConnection(
        configuration=configuration, session_ticket_handler=session_ticket_handler
    )

    # explicitly enable IPv4/IPv6 dual stack
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    completed = False
    try:
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        sock.bind((local_host, local_port, 0, 0))
        completed = True
    finally:
        if not completed:
            sock.close()
    # connect
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: create_protocol(connection, stream_handler=stream_handler),
        sock=sock,
    )
    protocol = cast(QuicConnectionProtocol, protocol)
    try:
        protocol.connect(addr)
        if wait_connected:
            await protocol.wait_connected()
        yield protocol
    finally:
        protocol.close()
        await protocol.wait_closed()
        transport.close()