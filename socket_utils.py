import socket
import sys

MAX_DATAGRAM_BITS = 65535 * 8
HEADER_SIZE = 160
MAX_PAYLOAD = MAX_DATAGRAM_BITS - HEADER_SIZE


def listen_socket(socket):
    conn, addr = socket.accept()
    print("Conexao recebida de: {}".format(str(addr)))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Dados recebidos: {}".format(readIPV4(data)))


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
        send_message(connecting, message)

    finally:
        print('Fechando conexão')
        connecting.close()


def send_message(socket, message):
    for datagram in createIPV4(socket.getsockname()[0], message):
        socket.sendall(bytearray(datagram, 'utf-8'))


# Cria o cabeçalho IPV4
def createIPV4(orig, payload):
    # ipv4 = 4
    version = binary_ip('4', 4)
    # 5 é o protocolo sem a parte de options
    ihl = binary_ip('5', 4)
    # requerido pelo professor
    typeOfService = binary_ip('0', 8)
    # requerido pelo professor
    flags = binary_ip('0', 3)
    # requerido pelo professor
    fragmentOffset = binary_ip('0', 13)
    # requerido pelo professor
    timeToLive = binary_ip('7', 8)
    # tcp = bin(6. Professor requeriu 0)
    protocol = binary_ip('6', 8)
    # requerido pelo professor
    headerChecksum = binary_ip('0', 16)

    # transforma cada parte do IP de origem em binario
    aux = orig.split('.')
    sourceIpAddress = binary_ip(aux[0], 8)
    sourceIpAddress = sourceIpAddress + binary_ip(aux[1], 8)
    sourceIpAddress = sourceIpAddress + binary_ip(aux[2], 8)
    sourceIpAddress = sourceIpAddress + binary_ip(aux[3], 8)
    # professor falou que só vamos utilizar na ultima versão
    destinationIpAddress = binary_ip('0', 32)

    finish = False
    frag = 0
    resp_list = []
    fragment_payload = payload
    while not finish:
        if sys.getsizeof(fragment_payload) > MAX_PAYLOAD:
            fragment_payload = payload[frag * MAX_PAYLOAD:
                                       frag * (MAX_PAYLOAD + 1)]
        else:
            finish = True

        # 16 bits. Identificador utilizado em caso de fragmentação
        identification = binary_ip(str(frag), 16)

        # 16 bits. tamanho do cabeçalho + carga útil
        totalLenght = binary_ip(str(160 + sys.getsizeof(fragment_payload)), 16)

        resp_list.append(
            version + ihl + typeOfService + totalLenght + identification +
            flags + fragmentOffset + timeToLive + protocol + headerChecksum +
            sourceIpAddress + destinationIpAddress + fragment_payload)

        frag += 1

    return resp_list


def readIPV4(datagram):
    version = int(datagram[:4], 2)

    ihl = int(datagram[4:8], 2)

    typeOfService = int(datagram[8:16], 2)

    totalLenght = int(datagram[16:32], 2)

    identification = int(datagram[32:48], 2)

    flags = int(datagram[48:51], 2)

    fragmentOffset = int(datagram[51:64], 2)

    timeToLive = int(datagram[64:72], 2)

    protocol = int(datagram[72:80], 2)

    headerChecksum = int(datagram[80:96], 2)

    sourceIpAddress = decimal_ip(datagram[96:128])

    destinationIpAddress = decimal_ip(datagram[128:160])

    payload = str(datagram[160:])

    answer_dict = {
        'version': str(version),
        'ihl': str(ihl),
        'typeOfService': str(typeOfService),
        'totalLenght': str(totalLenght),
        'identification': str(identification),
        'flags': str(flags),
        'fragmentOffset': str(fragmentOffset),
        'timeToLive': str(timeToLive),
        'protocol': str(protocol),
        'headerChecksum': str(headerChecksum),
        'sourceIpAddress': sourceIpAddress,
        'destinationIpAddress': destinationIpAddress,
        'payload': payload
    }

    return answer_dict


# Transforma o IP de binário para decimal
def decimal_ip(ip):
    k = 0
    resp = ''
    for i in range(1, 5):
        aux = 0
        for j in range(7, -1, -1):
            aux = aux + (2 ** j) * int(ip[k])
            k = k + 1
        resp = resp + str(aux) + '.'
    return resp[0:len(resp) - 1]


# Transforma em binario e completa com 0, para dar o tamanho necessario de bits
def binary_ip(value, length):
    answer = bin(int(value))[2:]
    zeros = ''
    for a in range(0, length - len(answer)):
        zeros = '0' + zeros
    return zeros + answer

# Valida a máscara da sub rede
def validaMascara(address, classe):
    if classe == 'A':
        size = 1
    elif classe == 'B':
        size = 2
    else:
        size = 3
    for j in range (0, size):
        if address.split('.')[j] != '255' and address.split('.')[j] != '0':
            return False
    return True

# Verifica a classe do endereço
def checkClass(address):
    if int(address.split('.')[0]) >= 0 and int(address.split('.')[0]) < 127:
        return 'A'
    elif int(address.split('.')[0]) > 127 and int(address.split('.')[0]) < 192:
        return 'B'
    else:
        return 'C'