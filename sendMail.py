from string import Template
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configparser import SafeConfigParser
from _getconfig import getConfig
import smtplib, codecs, sys, os.path


class enviaEmail:

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    config = getConfig.config()

    def DBexistente(dados, autor, email_autor, database, server):
        with open(enviaEmail.PROJECT_ROOT + '/templates/tpl0002.html', 'r') as html:
            template = Template(html.read())
            content  = template.substitute(autor = autor, database = database, servidor = server)
    
        msg = MIMEMultipart()
        msg['from'] = dados['para']
        msg['to']   = email_autor
        msg['subject'] = 'Importer Multi24H - Base ' + database

        corpo = MIMEText(content, 'html')
        msg.attach(corpo)
        return msg


    def DBimportada(dados, autor, email_autor, database, server):
        with open(enviaEmail.PROJECT_ROOT + '/templates/tpl0001.html', 'r') as html:
            template = Template(html.read())
            content  = template.substitute(autor = autor, database = database, servidor = server)
    
        msg = MIMEMultipart()
        msg['from'] = dados['para']
        msg['to']   = email_autor
        msg['subject'] = 'Importer Multi24H - Base ' + database

        corpo = MIMEText(content, 'html')
        msg.attach(corpo)
        return msg

    
    def envia(cod, autor, email_autor, database, server, file):
        try:
            # monta nome do banco
            database = database.split('_')
            database = database[0] + '_' + database[1] + '_' + database[2]

            # busca dados do config
            dados = enviaEmail.config

            # monta email de acordo com o codigo passado por parametro
            switcher={
                    1:enviaEmail.DBexistente(dados, autor, email_autor, database, server),
                    2:enviaEmail.DBimportada(dados, autor, email_autor, database, server)
                }

            # atribui o corpo do email na variavel msg
            msg = switcher.get(cod)
        except Exception as err:
            file.write("Houve erro ao criar o e-mail. \n {} \n" . format( str(err) ))
        
        # envia o email
        try:
            with smtplib.SMTP(dados['host'], dados['port']) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(dados['email'], dados['senha'])
                smtp.send_message(msg)
                file.write("E-mail enviado para solicitante \n ")
        except Exception as err:
            file.write("Ocorreram erros no envio de e-mail: \n " + str(err) + "\n")

