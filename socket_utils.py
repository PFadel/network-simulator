import socket


def listen_socket(socket):
    choice = ''
    #while True:
    #print('Aguardando conexao')
    conn, addr = socket.accept()
    print("Connection from: " + str(addr))
    while True:
        data = conn.recv(1024).decode()
        if not data:
           break
        print("Dados recebidos: " + str(data))
        break
        #while True:
         #   print('Deseja continuar ouvindo conexoes ? y/n')
          #  choice = input().lower()
           # if choice != 'y' and choice != 'n':
            #    print('Opcao invalida!')
             #   continue
            #break
        #if choice == 'n':
         #   break


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
		
#Transforma em binario e completa com 0, para dar o tamanho necessario de bits		
def toBin(value, length):
    answer = bin(int(value))[2:]
    zeros = ''
    for a in range (0 , 8 - len(answer)):
        zeros = '0' + zeros
    return zeros + answer

#Cria o cabeçalho IPV4	
def createIPV4(orig, dest, dados):
    version = '0100' #ipv4 = 4
    ihl = '0101' #5 é o protocolo sem a parte de options
    typeOfService = '00000000' #requerido pelo professor
    totalLenght = '?' #16 bits. tamanho do cabeçalho + carga útil
    identification = '?' # 	16 bits. Identificador utilizado em caso de fragmentação
    flags = '000' #requerido pelo professor
    fragmentOffset = '0000000000000' #requerido pelo professor
    timeToLive = '00000111' #requerido pelo professor
    protocol = '00000000' #tcp = 6. Professor requeriu 0
    headerChecksum = '0000000000000000' #requerido pelo professor
    
	#transforma cada parte do IP de origem em binario
    #origens = orig.split('.')
    sourceIpAddress = ''
    sourceIpAddress = toBin(orig, 8)
    #for i in range (0, len(origens)):
     #   sourceIpAddress = sourceIpAddress + toBin(origens[i], 8)	
    destinationIpAddress = '?' #professor falou que só vamos utilizar na ultima versão
    return version + ihl + typeOfService + totalLenght + identification + flags + fragmentOffset + timeToLive + protocol + headerChecksum + sourceIpAddress + destinationIpAddress + dados

def readIPV4(datagram):
    version = 4  #ipv4 = 4
    ihl = 5 #5 é o protocolo sem a parte de options
    typeOfService = 0 #requerido pelo professor
    totalLenght = '?' #16 bits. tamanho do cabeçalho + carga útil
    identification = '?' # 	16 bits. Identificador utilizado em caso de fragmentação
    flags = '000' #requerido pelo professor
    fragmentOffset = 0 #requerido pelo professor
    timeToLive = 7 #requerido pelo professor
    protocol = 0 #tcp = 6. Professor requeriu 0
    headerChecksum = 0 #requerido pelo professor
    sourceIpAddress = toDec(datagram[95:127])
     #   sourceIpAddress = sourceIpAddress + toBin(origens[i], 8)	
    destinationIpAddress = '?' #professor falou que só vamos utilizar na ultima versão
    return version + ihl + typeOfService + totalLenght + identification + flags + fragmentOffset + timeToLive + protocol + headerChecksum + sourceIpAddress + destinationIpAddress + dados

#Transforma o IP de binário para decimal
def toDec(ip):
    k = 0
    resp = ''
    for i in range(1,5):
        aux = 0
        for j in range(7,0, -1):
            aux = aux + (2 ** j) * int(ip[k])
            k= k+1
        resp = resp + str(aux) + '.'
    return resp[0:len(resp)]