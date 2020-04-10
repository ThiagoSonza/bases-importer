import psycopg2
from _getconfig import getConfig


class connect:
    
    # conecta no database intranet
    def connectDB():
        connection = psycopg2.connect(user      = "tecnos",
                                      password  = "pos200",
                                      host      = "192.168.22.242",
                                      port      = "5432",
                                      database  = "intranet")
        
        return connection
    
    # conecta no database do servidor/host onde ta instalado o app
    def connectDB2():
        config     = getConfig.config()

        connection = psycopg2.connect(user      = config['user'],
                                      password  = config['password'],
                                      host      = config['server'],
                                      port      = '5432',
                                      database  = 'postgres'
        )

        return connection

