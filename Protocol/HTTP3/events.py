from dataclasses import dataclass
from typing import List, Optional, Tuple

Headers = List[Tuple[bytes, bytes]]


class H3Event:
    """
    HTPP EVENT
    """


@dataclass
class DataReceived(H3Event):
    data: bytes

    stream_id: int

    stream_ended: bool

    push_id: Optional[int] = None


@dataclass
class DatagramReceived(H3Event):

    data: bytes

    flow_id: int


@dataclass
class HeadersReceived(H3Event):

    headers: Headers

    stream_id: int

    stream_ended: bool

    push_id: Optional[int] = None


@dataclass
class PushPromiseReceived(H3Event):

    headers: Headers

    push_id: int

    stream_id: int


@dataclass
class WebTransportStreamDataReceived(H3Event):
    data: bytes

    stream_id: int

    stream_ended: bool

    session_id: int