

# Realiza a validacao dos arquivos
def validate_args(neighbors, IPs, routing, args):
    interface_error = False
    mask_error = False

    max_value_neig = len(neighbors) - 1

    max_value_IPs = len(IPs) - 1

    max_value_routing = len(routing) - 1

    for i in range(0, max_value_routing):
        split_route = routing[i].split(' ')
        if len(split_route) != 3:
            print("Arquivo de roteamento em formato desconhecido")
            return False

        route_index = int(split_route[2])
        route_mask = split_route[1]
        route_class = split_route[0]

        if route_index > max_value_neig or route_index < 0:
            interface_error = True

        if mask_has_errors(route_mask, check_class(route_class)):
            mask_error = True
    # Se quantidade de IPs é diferente da quantidade de vizinhos, não existe indice da interface ou possui uma máscara invalida, retorna erro.
    if max_value_IPs != max_value_neig or interface_error or mask_error:
        if interface_error:
            print("Indice da interface nao existe.")
        elif mask_error:
            print("Mascara invalida")
        else:
            print("Quantidade de IPs e de Vizinhos deve ser igual")
        return False

    return True


# Valida a máscara da sub rede utilizando classes
def mask_has_errors(address, classe):
    if classe == 'A':
        size = 1
    elif classe == 'B':
        size = 2
    else:
        size = 3
    for j in range(0, size):
        add = address.split('.')[j]
        if add != '255' and add != '0':
            return True
    return False


# Verifica a classe do endereço
def check_class(address):
    add = address.split('.')[0]
    if int(add) >= 0 and int(add) < 127:
        return 'A'
    elif int(add) > 127 and int(add) < 192:
        return 'B'
    else:
        return 'C'
