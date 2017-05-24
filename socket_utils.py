import socket


def listen_socket(socket):
    choice = ''
    while True:
        print('Aguardando conexao')
        conn, addr = socket.accept()
        print("Connection from: " + str(addr))
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print("Dados recebidos: " + str(data))
        while True:
            print('Deseja continuar ouvindo conexoes ? y/n')
            choice = input().lower()
            if choice != 'y' and choice != 'n':
                print('Opcao invalida!')
                continue
            break
        if choice == 'n':
            break


def connect_to_neighboor(address):
    print('Tentando se conectar com vizinho {} {}'.format(address[0],
                                                          int(address[1])))
    server_address = (address[0], int(address[1]))
    connecting = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connecting.connect(server_address)
    try:
        print('Entre com a mensagem que deseja enviar')
        message = input()
        print('Enviando {}'.format(message))
        connecting.sendall(bytearray(message, 'utf-8'))

    finally:
        print('closing connection')
        connecting.close()
