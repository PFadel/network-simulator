import socket
import argparse
import socket_utils
import _thread

#Parameters
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="aplication desired port", type=int)
parser.add_argument("neighbors", help="path to neighbors file")
parser.add_argument("IPs", help="path to IPs file")
args = parser.parse_args()

port = args.port if args.port is not None else 10000

#Open documents
with open(args.neighbors, 'r') as neighbors_file:
    neighbors = neighbors_file.read().split('\n')
max_value_neig= len(neighbors) - 1

with open(args.IPs, 'r') as IPs_file:
    IPs = IPs_file.read().split('\n')
max_value_IPs= len(IPs) - 1

#Create a TCP/IP socket
listening = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind the socket to the port
server_address = ('', port)
print('starting up on {}'.format(server_address))
listening.bind(server_address)

listening.listen(1)

while True:
    if max_value_IPs != max_value_neig:
        print("Quantidade de IPs e de Vizinhos deve ser igual")
        continue
    _thread.start_new_thread(socket_utils.listen_socket, tuple([listening,]))
    print('Com qual vizinho se deseja conectar ?')
    for i, n in enumerate(neighbors):
        print('[{}] {}'.format(i, n))
    print('[{}] Desejo apenas receber conexões'.format(max_value_neig + 1))
    print('[{}] Terminar execução'.format(max_value_neig + 2))
    try:
        chosen = int(input())
    except ValueError:
        print('Escolha invalida, deve ser um valor inteiro')
        continue
    if chosen == max_value_neig + 1:
        socket_utils.listen_socket(listening)
    elif chosen == max_value_neig + 2:
        break
    elif chosen < 0 or chosen > max_value_neig:
        print('Escolha invalida, deve ser um valor entre 0 e {}'.format(
            max_value_neig))
        continue
    else:
        address = neighbors[chosen].split(' ')
        print(socket_utils.toDec(socket_utils.toBin('127', 8) + socket_utils.toBin('0', 8) + socket_utils.toBin('0', 8) + socket_utils.toBin('1', 8)))
        #socket_utils.connect_to_neighboor(address)      
print('Execution finished')
