from __future__ import print_function
import httplib2
import os, io
import GoogleAuth

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class actArvhives:

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/drive-python-quickstart.json
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = PROJECT_ROOT + '/config/google/client_secret.json'
    APPLICATION_NAME = 'Bases Importer'
    authInst = GoogleAuth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
    credentials = authInst.getCredentials()
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)

    def listFiles(size):
        results = actArvhives.drive_service.files().list(
            pageSize=size,fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))


    def uploadFile(filename,filepath,mimetype):
        file_metadata = {'name': filename}
        media = MediaFileUpload(filepath,
                                mimetype=mimetype)
        file = actArvhives.drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))


    def downloadFile(file_id, filepath, file_log):
        try:
            request = actArvhives.drive_service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                # print("Download %d%%." % int(status.progress() * 100))
            with io.open(filepath,'wb') as f:
                fh.seek(0)
                f.write(fh.read())
        except Exception as err:
            file_log.write("Erro no download do arquivo ID {} \n {} \n" . format(file_id, err))


    def createFolder(name):
        file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
        }
        file = actArvhives.drive_service.files().create(body=file_metadata, fields='id').execute()
        print ('Folder ID: %s' % file.get('id'))
        

    def searchFile(size,query):
        results = actArvhives.drive_service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(item)
                print('{0} ({1})'.format(item['name'], item['id']))


#uploadFile('unnamed.jpg','unnamed.jpg','image/jpeg')
#downloadFile('1Knxs5kRAMnoH5fivGeNsdrj_SIgLiqzV','google.jpg')
#createFolder('Google')
# searchFile(10,"name contains 'Getting'")