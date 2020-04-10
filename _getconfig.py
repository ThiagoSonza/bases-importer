from configparser import SafeConfigParser
import os

class getConfig:

    def config():
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        parser = SafeConfigParser()
        parser.read(PROJECT_ROOT + '/config/config.ini')

        host         = parser.get('config', 'host')
        port         = parser.get('config', 'port')
        email        = parser.get('config', 'email')
        senha        = parser.get('config', 'senha')
        para         = parser.get('config', 'from')
        server       = parser.get('server', 'server')
        path_origem  = parser.get('server', 'path_origem')
        path_destino = parser.get('server', 'path_destino')
        user         = parser.get('database', 'user')
        password     = parser.get('database', 'pass')
        
        config = {
            'host': host, # posicao 0
            'port': port,  # posicao 1
            'email': email,  # posicao 2
            'senha': senha,  # posicao 3
            'para': para,  # posicao 4
            'server': server,  # posicao 5
            'path_origem': path_origem,  # posicao 6
            'path_destino': path_destino,  # posicao 7
            'user' : user,  # posicao 8
            'password' : password  # posicao 9
            }       

        return config

