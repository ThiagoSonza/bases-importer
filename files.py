import os, shutil, os.path
from os import listdir
from os.path import isfile, join, basename
from configparser import SafeConfigParser
from _getconfig import getConfig


class files:

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    config = getConfig.config()
    
    def moveFiles(log):
        for item in [join(files.config['path_origem'], f) for f in listdir(files.config['path_origem']) if isfile(join(files.config['path_origem'], f)) and f.endswith('txt')]:
            try:
                shutil.move(item, join(files.config['path_destino'], basename(item)))
                # file.write("Arquivo {} movido da pasta {} para pasta {} \n" . format(basename(item), files.path_origem, files.path_destino))
            except Exception as err:
                log.write("Erro ao mover arquivo {} \n {} \n" . format(item, err))                

    
    def limpaImportados(log):
        dir = os.listdir(files.config['path_destino'])
        for file in dir:
            try:
                os.remove(files.config['path_destino'] + "/" + file)
            except Exception as err:
                log.write("Erro ao remover arquivo {} \n  {} \n" . format(file, err))

