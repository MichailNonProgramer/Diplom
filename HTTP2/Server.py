import json
import socket

import h2.connection
import h2.events
import h2.config


def send_response(conn, event):
    stream_id = event.stream_id
    response_data = json.dumps(dict(event.headers)).encode('utf-8')

    conn.send_headers(
        stream_id=stream_id,
        headers=[
            (':status', '200'),
            ('server', 'basic-h2-server/1.0'),
            ('content-length', str(len(response_data))),
            ('content-type', 'application/json'),
        ],
    )
    conn.send_data(
        stream_id=stream_id,
        data=response_data,
        end_stream=True
    )


def handle(sock):
    config = h2.config.H2Configuration()
    config.validate_outbound_headers = False
    config.validate_inbound_headers = False
    config.normalize_outbound_headers = False
    conn = h2.connection.H2Connection(config=config)
    conn.initiate_connection()
    sock.sendall(conn.data_to_send())

    try:
        while True:
            data = sock.recv(65535)
            if not data:
                break
            print(data)
            events = conn.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.RequestReceived):
                    send_response(conn, event)

            data_to_send = conn.data_to_send()
            if data_to_send:
                sock.sendall(data_to_send)
    except Exception:
        pass


sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 443))
sock.listen(5)

while True:
    handle(sock.accept()[0])
