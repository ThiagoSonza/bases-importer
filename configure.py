#!/usr/bin/python3
from configparser import SafeConfigParser
import os.path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

print("--------------------------------------------------------- ")
print("Bem vindo ao Configurador do App para Importação de Bases ")
print("--------------------------------------------------------- ")
print("Observe alguns detalhes: ")
print("Ao informar o caminho das pastas, informe a partir do diretório da Aplicação, ou seja, a partir de onde está o arquivo main.py ")
print("Por exemplo: para o diretório bases, você informará: ../bases/ e para o diretório de bases importadas: ../bases/importados/ \n")

# solicita informações para usuário
host  = input("Informe o Servidor SMTP..........: ")
port  = input("Informe a Porta do Servidor SMTP.: ")
email = input("Informe o E-mail de envio........: ")
senha = input("Informe a senha do E-mail........: ")
efrom = input("Informe o nome da Conta de E-mail: ")

server       = input("Informe o IP do servidor local..: ")
path_origem  = input("Informe o caminho da pasta onde ficarão os arquivos GZ: ")
path_destino = input("Informe o caminho da pasta onde ficarão os arquivos TXT importados: ")

userDB = input("Informe o usuário para importação de bases.......: ")
passDB = input("Digite a senha do usuário do banco para importação: ")

# cria o arquivo e grava as informações nele
parser = SafeConfigParser()
cgfile = open(PROJECT_ROOT + '/config/config.ini','w')
        
parser.add_section('config')
parser.set('config', 'host', host)
parser.set('config', 'port', port)
parser.set('config', 'email', email)
parser.set('config', 'senha', senha)
parser.set('config', 'from', efrom)

parser.add_section('server')
parser.set('server', 'ip', server)
parser.set('server', 'path_origem', path_origem)
parser.set('server', 'path_destino', path_destino)

parser.add_section('database')
parser.set('database', 'user', userDB)
parser.set('database', 'pass', passDB)

parser.write(cgfile)
cgfile.close()