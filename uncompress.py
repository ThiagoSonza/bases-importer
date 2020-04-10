import gzip, shutil, os.path
from _getconfig import getConfig


class uncompressFile:
    try:
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        config = getConfig.config()
    except Exception:
        pass


    def descompactaGZ(log, arquivoGZ):
        arquivoTXT = arquivoGZ[:-3]

        try:
            with gzip.open(uncompressFile.PROJECT_ROOT + '/' + uncompressFile.config['path_origem'] + arquivoGZ, 'rb') as entrada:
                with open(uncompressFile.PROJECT_ROOT + '/' + uncompressFile.config['path_origem'] + arquivoTXT, 'wb') as saida:
                    shutil.copyfileobj(entrada, saida)
            log.write('Arquivo {} descompactado \n' . format(arquivoGZ))
            return arquivoTXT
        except Exception as err:
            log.write("Erro ao descompactar arquivo {} \n {} \n" . format(arquivoGZ, err))

