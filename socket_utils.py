import socket


def listen_socket(socket):
    conn, addr = socket.accept()
    print("Connection from: " + str(addr))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Dados recebidos: " + readIPV4(data))


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
        connecting.sendall(
            bytearray(createIPV4('127.0.0.1', message), 'utf-8'))

    finally:
        print('closing connection')
        connecting.close()


# Cria o cabeçalho IPV4
def createIPV4(orig, payload):
    # ipv4 = 4
    version = binary_ip('4',4)
    # 5 é o protocolo sem a parte de options
    ihl = binary_ip('5',4)
    # requerido pelo professor
    typeOfService = binary_ip('0', 8)
    # 16 bits. tamanho do cabeçalho + carga útil   ------------------------------------------------
    totalLenght = binary_ip('0', 16)
    # 16 bits. Identificador utilizado em caso de fragmentação -------------------------------
    identification = binary_ip('0', 16)
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
    # professor falou que só vamos utilizar na ultima versão             -------------------------------------------
    destinationIpAddress = binary_ip('0', 32)
    return version +\
        ihl +\
        typeOfService +\
        totalLenght +\
        identification +\
        flags +\
        fragmentOffset +\
        timeToLive +\
        protocol +\
        headerChecksum +\
        sourceIpAddress +\
        destinationIpAddress +\
        payload

def readIPV4(datagram):
    #print("RECEBI UM DATAGRAMA DE LEN {}".format(len(datagram)))
    #print("datagrama" + datagram)
    # ipv4 = 4
    version = int(datagram[:4], 2)
    #print("A" + version)
    # 5 é o protocolo sem a parte de options
    ihl = int(datagram[4:8],2)
    #print("B" + ihl) 
 # requerido pelo professor
    typeOfService = int(datagram[8:16],2)
    #print("C" + typeOfService) 
 # 16 bits. tamanho do cabeçalho + carga útil
    totalLenght = int(datagram[16:32],2)
    #print("D" + totalLenght)
	# 16 bits. Identificador utilizado em caso de fragmentação
    identification = int(datagram[32:48],2)
    #print("E" + identification)
    # requerido pelo professor
    flags = int(datagram[48:51],2)
    #print("F" + flags)
	# requerido pelo professor
    fragmentOffset = int(datagram[51:64],2)
    #print("G" + fragmentOffset)
	# requerido pelo professor
    timeToLive = int(datagram[64:72],2)
    #print("H" + timeToLive)
	# tcp = 6. Professor requeriu 0
    protocol = int(datagram[72:80],2)
    #print("I" + protocol)
    # requerido pelo professor
    headerChecksum = int(datagram[80:96],2)
    #print("J" + headerChecksum)    
    #print("gabiru" + datagram[96:128])
    sourceIpAddress = decimal_ip(datagram[96:128])
    #print("K" + sourceIpAddress)    
	# professor falou que só vamos utilizar na ultima versão
    destinationIpAddress = decimal_ip(datagram[128:160])
    #print("L" + destinationIpAddress)
    payload = str(datagram[160:])
    return str(version) +\
        str(ihl) +\
        str(typeOfService) +\
        str(totalLenght) +\
        str(identification) +\
        str(flags) +\
        str(fragmentOffset) +\
        str(timeToLive) +\
        str(protocol) +\
        str(headerChecksum) +\
        sourceIpAddress +\
        destinationIpAddress +\
        payload
    #return payload


# Transforma o IP de binário para decimal
def decimal_ip(ip):
    #print("Recebi" + ip)
    k = 0
    resp = ''
    for i in range(1,5):
        aux = 0
        for j in range(7,-1, -1):
            aux = aux + (2 ** j) * int(ip[k])
            k= k+1
        resp = resp + str(aux) + '.'
    return resp[0:len(resp)-1]
		#print("Retornarei" + resp[0:len(resp)-1])


# Transforma em binario e completa com 0, para dar o tamanho necessario de bits
def binary_ip(value, length):
    answer = bin(int(value))[2:]
    zeros = ''
    for a in range(0, length - len(answer)):
        zeros = '0' + zeros
    return zeros + answer
