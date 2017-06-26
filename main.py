import socket
import socket_utils
import _thread


def main(neighbors, IPs, routing, port):
    # Cria os sockets e realiza os devidos binds.
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
    # Menu principal
    while True:
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
