from dataclasses import dataclass
from typing import Optional


class QuicEvent:

    pass


@dataclass
class ConnectionIdIssued(QuicEvent):
    connection_id: bytes


@dataclass
class ConnectionIdRetired(QuicEvent):
    connection_id: bytes


@dataclass
class ConnectionTerminated(QuicEvent):

    error_code: int

    frame_type: Optional[int]

    reason_phrase: str


@dataclass
class DatagramFrameReceived(QuicEvent):

    data: bytes



@dataclass
class HandshakeCompleted(QuicEvent):

    alpn_protocol: Optional[str]

    early_data_accepted: bool

    session_resumed: bool


@dataclass
class PingAcknowledged(QuicEvent):

    uid: int


@dataclass
class ProtocolNegotiated(QuicEvent):

    alpn_protocol: Optional[str]


@dataclass
class StreamDataReceived(QuicEvent):

    data: bytes

    end_stream: bool

    stream_id: int


@dataclass
class StreamReset(QuicEvent):

    error_code: int

    stream_id: int