import socket
import socket_utils
import _thread


def main(neighbors, IPs, routing, port):
    max_value = len(routing) - 1
    # Create a TCP/IP socket

    # Bind the socket to the port

    out_sockets = []
    for i in IPs:
        listening = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (i.split(' ')[0], port)
        print('Iniciando bind em: {}'.format(server_address))
        listening.bind(server_address)
        listening.listen(1)
        _thread.start_new_thread(socket_utils.listen_socket,
                                 tuple([neighbors, listening, routing]))
        out_sockets.append(listening)

    while True:

        """"print('Para qual no da rede se deseja enviar uma mensagem ?')

        for i, n in enumerate(neighbors):
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
            route = neighbors[chosen].split(' ')[0]
            socket_utils.route_message(neighbors, routing, route)
"""
        option = ''
        print('Digite 1 para enviar mensagem ou 2 para sair.')
        try:
            option = int(input())
        except ValueError:
            print('Escolha invalida, deve ser um valor inteiro.')
        if option == 1:
            print('Digite o IP de destino:')
            destination = input()
            print('Digite a porta:')
            port = input()
            socket_utils.route_message(neighbors, routing, destination)
        elif option == 2:
            break   
    print('Execucao terminada')
