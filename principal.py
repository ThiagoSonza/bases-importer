from _conn import connect
from _getconfig import getConfig
from sendMail import enviaEmail
from uncompress import uncompressFile
from importaDB import importa
from files import files
from GoogleAuth import auth
from GoogleArchives import actArvhives

import datetime, shutil, os, os.path
from os import listdir
from os.path import isfile, join, basename


class principal:

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    config = getConfig.config()
    # parser = SafeConfigParser()
    # parser.read(PROJECT_ROOT + '/config/config.ini')
    # server      = parser.get('server', 'server')
    # path_origem = PROJECT_ROOT + "/" + parser.get('server', 'path_origem')

    def consulta(server):
        getConn = connect.connectDB()
        cursor = getConn.cursor()
        cursor.execute("SELECT id,autor,email,fileid,backup,server FROM agendamentos WHERE server = '{}' and baixado = {} and importado = {};" . format(server, False, False))
        agendamentos = cursor.fetchall()
        cursor.close()
        getConn.close()
        return agendamentos


    def atualizaSituacao(cod, agendamento, file):
        # cod 1 = atualiza flag baixado
        # cod 2 = atualiza flag importado
        try:
            getConn = connect.connectDB()
            cursor  = getConn.cursor()
            if (cod == 1):
                cursor.execute("UPDATE agendamentos SET baixado = {} WHERE id = {} RETURNING backup;" . format(True, agendamento[0]))
                file.write("Atualizado situação BAIXADO para agendamento ID: {} \n" . format( agendamento[0] ))
            else:
                cursor.execute("UPDATE agendamentos SET importado = {} WHERE id = {} RETURNING backup;" . format(True, agendamento[0]))
                file.write("Atualizado situação IMPORTADO para agendamento ID: {} \n" . format( agendamento[0] ))
            getConn.commit()
            cursor.close()
            getConn.close()
        except Exception as err:
            file.write("Erro ao atualizar situação {} do agendamento {} \n {} \n" . format(cod, agendamento, err))
    

    def main():
        file = open(principal.PROJECT_ROOT + "/logs/log.txt","w+")
        file.write("################################################# \n")
        file.write(str(datetime.datetime.now()) +  " - Inicilizando Rotinas \n")
        file.write("################################################# \n")

        # limpa pasta importados
        files.limpaImportados(file)

        # busca agendamentos para esse server e grava no arquivo log        
        agendamentos = principal.consulta(principal.config['server'])
        for agendamento in agendamentos:
            file.write("Agendamento encontrado: " + str(agendamento) + "\n")
            # cria o DB
            existeDB = importa.criaDB(agendamento[4], file)

            if existeDB is False:
                # atualiza flag baixado para true
                principal.atualizaSituacao(1, agendamento, file)

                # atualiza flag importado para true
                principal.atualizaSituacao(2, agendamento, file)

                # envia email para autor informando BD existente
                enviaEmail.envia(1, agendamento[1], agendamento[2], agendamento[4], agendamento[5], file)
                
            else:
                # faz download do arquivo de backup
                actArvhives.downloadFile(agendamento[3], principal.config['path_origem'] + agendamento[4], file)
                
                # atualiza flag baixado para true
                principal.atualizaSituacao(1, agendamento, file)

                # descompactar arquivo backup
                arquivoTXT = uncompressFile.descompactaGZ(file, agendamento[4])

                # monta string nome banco e importa
                importa.importaDB(agendamento[4], arquivoTXT, file)
                
                # atualiza flag importado para true
                principal.atualizaSituacao(2, agendamento, file)

                # envia email para autor informando importação
                enviaEmail.envia(2, agendamento[1], agendamento[2], agendamento[4], agendamento[5], file)

        # move arquivos para pasta importados
        files.moveFiles(file)

        file.write("################################################ \n")
        file.write(str(datetime.datetime.now()) +  " - Finalizando Rotinas \n")
        file.write("################################################ \n")

        # fecha arquivo log
        file.close()

        