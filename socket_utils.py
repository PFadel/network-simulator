import socket
import sys

MAX_DATAGRAM_BITS = 65535 * 8
HEADER_SIZE = 160
MAX_PAYLOAD = MAX_DATAGRAM_BITS - HEADER_SIZE


# Identifica o socket a ser usado no roteamento
def find_socket_to_use(routing, route):
    diffs = []

    all_routes = None

    route = route.split('.')
    route = binary_ip(route[0], 8) + binary_ip(route[1], 8) + binary_ip(route[2], 8) + binary_ip(route[3], 8)

    for req in routing:
        req = req.split(' ')[0].split('.')
        req = binary_ip(req[0], 8) + binary_ip(req[1], 8) + binary_ip(req[2], 8) + binary_ip(req[3], 8)

        if req == binary_ip('0', 32):
            all_routes = req

        for i, c in enumerate(route):
            if req[i] != c:
                diffs.append(i)
                break
            if len(route) - 1 == i:
                diffs.append(i)

    longest_prefix = diffs[0]
    longest_prefix_index = 0

    for i, di in enumerate(diffs):
        if di > longest_prefix:
            longest_prefix = di
            longest_prefix_index = i

    if longest_prefix == 0:
        return all_routes
    return routing[longest_prefix_index]


# Recebe o datagrama, verificando se estamos no destino ou se precisamos reenviar o datagrama
def listen_socket(neighbors, socket, routing):
    while True:
        conn, addr = socket.accept()
        print("Conexao recebida de: {}".format(str(addr)))
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            dic = readIPV4(data)
            if socket.getsockname()[0] == dic["destinationIpAddress"]:
                print("Dados recebidos: {}".format(dic["payload"]))
            else:
                route_message(neighbors, routing, dic["destinationIpAddress"], data[HEADER_SIZE:], dic["timeToLive"])
                break


# Envia a mensagem para o vizinho correto baseado em sua tabela de roteamento
def route_message(neighbors, routing, route, message=None, ttl='7'):
    conn = find_socket_to_use(routing, route)

    if conn is None:
        print("Nenhuma rota encontrada para o destino, abortando envio")
        return
    if ttl == 0:
        print("Número de saltos chegou ao limite, abortando envio")
        return
    conn_index = int(conn.split(' ')[2])

    neighbor = neighbors[conn_index].split(' ')

    print('Abrindo conexao com: {} {}'.format(neighbor[0], int(neighbor[1])))
    server_route = (neighbor[0], int(neighbor[1]))
    connecting = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connecting.connect(server_route)
    try:
        if message is None:
            print('Entre com a mensagem que deseja enviar')
            message = input()
        print('Enviando {}'.format(message))
        send_message(connecting, route, message, ttl)

    finally:
        print('Fechando conexao')
        connecting.close()


# Encaminha a mensagem para o seu destino
def send_message(socket, destination, message, ttl):
    for datagram in createIPV4(socket.getsockname()[0], destination, message, ttl):
        socket.sendall(bytearray(datagram, 'utf-8'))


# Cria o cabeçalho IPV4
def createIPV4(orig, dest, payload, ttl):
    # ipv4 = 4
    version = binary_ip('4', 4)
    # 5 é o protocolo sem a parte de options
    ihl = binary_ip('5', 4)

    typeOfService = binary_ip('0', 8)

    flags = binary_ip('0', 3)

    fragmentOffset = binary_ip('0', 13)

    timeToLive = binary_ip(str(int(ttl) - 1), 8)

    protocol = binary_ip('6', 8)

    headerChecksum = binary_ip('0', 16)

    # transforma cada parte do IP de origem em binario
    aux = orig.split('.')
    sourceIpAddress = binary_ip(aux[0], 8)
    sourceIpAddress = sourceIpAddress + binary_ip(aux[1], 8)
    sourceIpAddress = sourceIpAddress + binary_ip(aux[2], 8)
    sourceIpAddress = sourceIpAddress + binary_ip(aux[3], 8)
    # transforma cada parte do IP de destino em binario
    aux = dest.split('.')
    destinationIpAddress = binary_ip(aux[0], 8)
    destinationIpAddress = destinationIpAddress + binary_ip(aux[1], 8)
    destinationIpAddress = destinationIpAddress + binary_ip(aux[2], 8)
    destinationIpAddress = destinationIpAddress + binary_ip(aux[3], 8)

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


# Realiza a decodificação do cabeçalho IPV4, retornando um dicionário.
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
