import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--host", help="aplication desired IP address")
parser.add_argument("-p", "--port", help="aplication desired port", type=int)
parser.add_argument("-l", "--length", help="length of chunks", type=int)
args = parser.parse_args()

host = args.host if args.host is not None else 'localhost'
port = args.port if args.port is not None else 10000
length = args.length if args.length is not None else 16

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (host, port)
print('connecting to {}'.format(server_address))
sock.connect(server_address)

try:
    # Send data
    message = 'This is the message.  It will be repeated.'
    print('sending {}'.format(message))
    sock.sendall(bytearray(message, 'utf-8'))

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(length)
        amount_received += len(data)
        print('received {}'.format(data))

finally:
    print('closing socket')
    sock.close()
