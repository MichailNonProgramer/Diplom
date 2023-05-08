import socket


serverAddressPort = ("127.0.0.1", 20001)

bufferSize = 1024

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)

# Send to server using created UDP socket
i = 0
while i < 10:
    msgFromClient = "Hello UDP Server" + "rei"*i*100

    bytesToSend = str.encode(msgFromClient)
    i = i + 1
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {} {}".format(i, msgFromServer[0])
    print(msg)
