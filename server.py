import socket
import argparse
import socket_utils
import _thread

# Parameters
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="aplication desired port", type=int)
parser.add_argument("neighbors", help="path to neighbors file")
parser.add_argument("IPs", help="path to IPs file")
parser.add_argument("Routing", help="path to Routing file")
args = parser.parse_args()

port = args.port if args.port is not None else 10000
erroInterface = False
erroMascara   = False
# Open documents
with open(args.neighbors, 'r') as neighbors_file:
    neighbors = neighbors_file.read().split('\n')
max_value_neig = len(neighbors) - 1
with open(args.IPs, 'r') as IPs_file:
    IPs = IPs_file.read().split('\n')
max_value_IPs = len(IPs) - 1

with open(args.Routing, 'r') as Routing_file:
    Routing = Routing_file.read().split('\n')
max_value_Routing = len(Routing) - 1
for i in range (0, max_value_Routing):
    if int(Routing[i].split(' ')[2]) > max_value_neig or int(Routing[i].split(' ')[2]) < 0:
            erroInterface = True
    if socket_utils.validaMascara(Routing[i].split(' ')[1],socket_utils.checkClass(Routing[i].split(' ')[0])):
        erroMascara = True
if max_value_IPs != max_value_neig or erroInterface or erroMascara:
    if erroInterface:
        print("Índice da interface não existe.")
    elif erroMascara:
        print("Máscara inválida")
    else:
        print("Quantidade de IPs e de Vizinhos deve ser igual")
else:
    # Create a TCP/IP socket
    listening = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('', port)
    print('starting up on {}'.format(server_address))
    listening.bind(server_address)

    listening.listen(1)

    while True:
        _thread.start_new_thread(socket_utils.listen_socket,
                                 tuple([listening, ]))
        print('Com qual vizinho se deseja conectar ?')
        for i, n in enumerate(neighbors):
            print('[{}] {}'.format(i, n))
        print('[{}] Terminar execução'.format(max_value_neig + 1))
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
print('Execution finished')
