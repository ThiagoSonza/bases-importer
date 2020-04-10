import os, os.path
from configparser import SafeConfigParser
from _conn import connect
from _getconfig import getConfig


class importa:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    config       = getConfig.config()

    def importaDB(database, arquivoTXT, file):
        # monta nome do banco
        database = database.split('_')
        database = database[0] + '_' + database[1] + '_' + database[2]
        
        # monta o comando e roda importação
        command = 'export PGPASSWORD=' + importa.config['password'] + ' && psql -h 192.168.22.231 -p 5432 -d ' + database + ' -U ' + importa.config['user'] + ' -w < ' + importa.config['path_origem'] + "/" + arquivoTXT
        os.system( command )
        file.write("Backup {} importado no banco {} \n" . format(arquivoTXT, database) )
            

    def criaDB(database, file):
        # monta nome do banco
        database = database.split('_')
        database = database[0] + '_' + database[1] + '_' + database[2]
        existeDB = False

        # verfica se já existe um BD com mesmo nome
        try:
            getConn = connect.connectDB2()
            cursor  = getConn.cursor()
            cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{}';" . format(database))
            exists = cursor.fetchone()

            # cria o banco ou retorna false
            if exists is None:
                command = 'export PGPASSWORD=' + importa.config['password'] + ' && createdb -h 192.168.22.231 -p 5432 -U ' + importa.config['user'] + ' ' + database + ' -T template2;'
                os.system(command)
                file.write('Banco de Dados {} criado \n' . format(database))
                existeDB = True
            else:
                file.write("Banco de Dados {} já existente. \n" . format(database))

            cursor.close()
            getConn.close()
        except Exception as err:
            file.write("Houve um erro ao se conectar no DB \n {} \n " . format(err) )

        return existeDB

