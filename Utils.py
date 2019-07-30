import gzip
import sh #import pg_dump
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError
import os
import datetime

class terminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

import globalVariables as gv

def nameFromPath(path):
    reversedPath = path[::-1]
    name = ""
    for char in reversedPath:
        if char != '/' and char != '\\':
            name = name + char
        else:
            break
    return name[::-1]

def removeDuplicateInAcquisti(acquisti):
    retList = []
    for acquisto in acquisti:
        if acquisto.product_id  not in list(map(lambda el: el.product_id, retList)):
            retList.append(acquisto)
    return retList

def getNumAcquisti(toCheck, acquisti):
    counter = 0
    for acquisto in acquisti:
        if toCheck.product_id == acquisto.product_id:
            counter += 1

    return counter

def removeOldBackups(dbx):
    try:
        current_year = datetime.date.today().year
        dbx.files_delete('/backup' + datetime.date.today().replace(year=current_year-1) + '.gz')
        print('Removed old backup')
        return
    except:
        print('No backup older than a year')
        return

def dropboxUpload(LOCALFILE):
    BACKUPPATH = '/backup' + str(datetime.date.today()) + '.gz'
    dbx = dropbox.Dropbox(os.environ["DROPBOX_API_KEY"])

    try:
        dbx.users_get_current_account()
    except AuthError:
        print("ERROR: Invalid access TOKEN")
        return

    removeOldBackups(dbx)

    with open(LOCALFILE, 'rb') as f:
        print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
            print("Backup succeded!")
            os.system('rm ' + LOCALFILE)
            return
        except ApiError as err:
            if (err.error.is_path() and err.error.get_path().reason.is_insufficient_space()):
                print("Spazio insufficiente, impossibile eseguire il backup")
                os.system("rm " + LOCALFILE)
                return
            elif err.user_message_text:
                print(err.user_message_text)
                return
            else:
                print(err)
                return

def dbBackup():
    url = gv.DB_URL
    list = url.split('/')[2:]
    user = list[0].split(':')[0]
    port = list[0].split(':')[2]
    host = list[0].split('@')[1].split(':')[0]
    password = list[0].split(':')[1].split('@')[0]
    db = list[1]
    print(user + port + host + password, sep="\t")


    os.environ["PGPASSWORD"] = password

    with gzip.open('backup.gz', 'wb') as f:
        sh.pg_dump('-h', host, '-U', user, db, '-p', port, _out=f)

    dropboxUpload('backup.gz')
