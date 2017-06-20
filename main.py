import socket
import socket_utils
import _thread


def main(neighbors, IPs, routing, port):
    max_value = len(routing) - 1
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
        print('Digite 1 para enviar mensagem ou 2 para sair')
        try:
            option = int(input())
        except ValueError:
            print('Escolha invalida, deve ser um valor inteiro')
            continue
        if option == 1:
            print('Digite a mensagem a ser enviada.')
            mensagem = input()
            print('Digite o ip de destino.')
            destination = input()
            print('Digite a porta.')
            port = input()
            socket_utils.route_message(neighbors, IPs, routing, destination)
        elif option == 2:
            break		
        """for i, n in enumerate(routing):
            print('[{}] {}'.format(i, n))
        print('[{}] Terminar execucao'.format(max_value + 1))
        try:
            chosen = int(input())
        except ValueError:
            print('Escolha invalida, deve ser um valor inteiro')
            continue
        if chosen == max_value + 1:
            break
        elif chosen < 0 or chosen > max_value:
            print('Escolha invalida, deve ser um valor entre 0 e {}'.format(
                max_value))
            continue
        else:
            route = routing[chosen].split(' ')[0]
            socket_utils.route_message(neighbors, IPs, routing, route)
"""
    print('Execucao terminada')
