import socket
import argparse
import socket_utils
import _thread

# Parameters
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="Porta desejada da aplicacao",
                    type=int)
parser.add_argument("neighbors", help="Caminho para o arquivo de vizinhos")
parser.add_argument("IPs", help="Caminho para o arquivo de IPs virtuais")
args = parser.parse_args()

port = args.port if args.port is not None else 10000

# Open documents
with open(args.neighbors, 'r') as neighbors_file:
    neighbors = neighbors_file.read().split('\n')
max_value_neig = len(neighbors) - 1

with open(args.IPs, 'r') as IPs_file:
    IPs = IPs_file.read().split('\n')
max_value_IPs = len(IPs) - 1

if max_value_IPs != max_value_neig:
    print("Quantidade de IPs e de Vizinhos deve ser igual")
else:
    # Create a TCP/IP socket
    listening = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('', port)
    print('Iniciando bind em: {}'.format(server_address))
    listening.bind(server_address)

    listening.listen(1)

    while True:
        _thread.start_new_thread(socket_utils.listen_socket,
                                 tuple([listening, ]))
        print('Com qual vizinho se deseja conectar ?')
        for i, n in enumerate(neighbors):
            print('[{}] {}'.format(i, n))
        print('[{}] Terminar execucao'.format(max_value_neig + 1))
        try:
            chosen = int(input())
        except ValueError:
            print('Escolha invalida, deve ser um valor inteiro')
            continue
        if chosen == max_value_neig + 1:
            break
        elif chosen < 0 or chosen > max_value_neig:
            print('Escolha invalida, deve ser um valor entre 0 e {}'.format(
                max_value_neig))
            continue
        else:
            address = neighbors[chosen].split(' ')
            socket_utils.connect_to_neighboor(address)

print('Execucao terminada')
