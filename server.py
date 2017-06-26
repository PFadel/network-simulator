import argparse
import validate
import main

# Define os parâmetros
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="Porta desejada da aplicacao",
                    type=int)
parser.add_argument("neighbors", help="Caminho para o arquivo de vizinhos")
parser.add_argument("IPs", help="Caminho para o arquivo de IPs virtuais")
parser.add_argument("routing",
                    help="Caminho para o arquivo da tabela de roteamento")
args = parser.parse_args()

port = args.port if args.port is not None else 10000

# Abre arquivos
with open(args.neighbors, 'r') as neighbors_file:
    neighbors = neighbors_file.read().split('\n')

with open(args.IPs, 'r') as IPs_file:
    IPs = IPs_file.read().split('\n')

with open(args.routing, 'r') as Routing_file:
    routing = Routing_file.read().split('\n')
# Realiza validações necessárias
if validate.validate_args(neighbors, IPs, routing, args):
    main.main(neighbors, IPs, routing, port)
