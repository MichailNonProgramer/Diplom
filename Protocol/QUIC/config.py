from dataclasses import dataclass, field
from os import PathLike
from re import split
from typing import Any, List, Optional, TextIO, Union

from ..tls import (
    CipherSuite,
    SessionTicket,
    load_pem_private_key,
    load_pem_x509_certificates,
)
from .logger import QuicLogger
from .packet import QuicProtocolVersion


@dataclass
class QuicConfiguration:

    alpn_protocols: Optional[List[str]] = None

    connection_id_length: int = 8

    idle_timeout: float = 60.0

    is_client: bool = True

    max_data: int = 1048576

    max_stream_data: int = 1048576

    quic_logger: Optional[QuicLogger] = None

    secrets_log_file: TextIO = None

    server_name: Optional[str] = None

    session_ticket: Optional[SessionTicket] = None

    cadata: Optional[bytes] = None
    cafile: Optional[str] = None
    capath: Optional[str] = None
    certificate: Any = None
    certificate_chain: List[Any] = field(default_factory=list)
    cipher_suites: Optional[List[CipherSuite]] = None
    initial_rtt: float = 0.1
    max_datagram_frame_size: Optional[int] = None
    private_key: Any = None
    quantum_readiness_test: bool = False
    supported_versions: List[int] = field(
        default_factory=lambda: [
            QuicProtocolVersion.VERSION_1,
            QuicProtocolVersion.DRAFT_32,
            QuicProtocolVersion.DRAFT_31,
            QuicProtocolVersion.DRAFT_30,
            QuicProtocolVersion.DRAFT_29,
        ]
    )
    verify_mode: Optional[int] = None

    def load_cert_chain(
        self,
        certfile: PathLike,
        keyfile: Optional[PathLike] = None,
        password: Optional[Union[bytes, str]] = None,
    ) -> None:
        with open(certfile, "rb") as fp:
            boundary = b"-----BEGIN PRIVATE KEY-----\n"
            chunks = split(b"\n" + boundary, fp.read())
            certificates = load_pem_x509_certificates(chunks[0])
            if len(chunks) == 2:
                private_key = boundary + chunks[1]
                self.private_key = load_pem_private_key(private_key)
        self.certificate = certificates[0]
        self.certificate_chain = certificates[1:]

        if keyfile is not None:
            with open(keyfile, "rb") as fp:
                self.private_key = load_pem_private_key(
                    fp.read(),
                    password=password.encode("utf8")
                    if isinstance(password, str)
                    else password,
                )

    def load_verify_locations(
        self,
        cafile: Optional[str] = None,
        capath: Optional[str] = None,
        cadata: Optional[bytes] = None,
    ) -> None:
        self.cafile = cafile
        self.capath = capath
        self.cadata = cadata