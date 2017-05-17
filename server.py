import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="aplication desired port", type=int)
parser.add_argument("neighbors", help="path to neighbors file")
args = parser.parse_args()

port = args.port if args.port is not None else 10000

with open(args.neighbors, 'r') as neighbors_file:
    neighbors = neighbors_file.read().split('\n')
max_value = len(neighbors) - 1

# Create a TCP/IP socket
listening = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', port)
print('starting up on {}'.format(server_address))
listening.bind(server_address)

listening.listen(1)

while True:
    # Wait for a connection
    print('Com qual vizinho se deseja conectar ?')
    for i, n in enumerate(neighbors):
        print('[{}] {}'.format(i, n))
    try:
        chosen = int(input())
    except ValueError:
        print('Escolha invalida, deve ser um valor inteiro')
        continue
    if chosen < 0 or chosen > max_value:
        print('Escolha invalida, deve ser um valor entre 0 e {}'.format(
            max_value))
        continue

    add = neighbors[chosen].split(' ')
    print('Tentando se conectar com vizinho {} {}'.format(add[0], int(add[1])))
    server_address = (add[0], int(add[1]))
    connecting = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connecting.connect(server_address)
