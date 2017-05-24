import socket
import argparse
import socket_utils

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
    print('Com qual vizinho se deseja conectar ?')
    for i, n in enumerate(neighbors):
        print('[{}] {}'.format(i, n))
    print('[{}] Desejo apenas receber conexões'.format(max_value + 1))
    print('[{}] Terminar execução'.format(max_value + 2))
    try:
        chosen = int(input())
    except ValueError:
        print('Escolha invalida, deve ser um valor inteiro')
        continue
    if chosen == max_value + 1:
        socket_utils.listen_socket(listening)
    elif chosen == max_value + 2:
        break
    elif chosen < 0 or chosen > max_value:
        print('Escolha invalida, deve ser um valor entre 0 e {}'.format(
            max_value))
        continue
    else:
        address = neighbors[chosen].split(' ')
        socket_utils.connect_to_neighboor(address)
print('Execution finished')
