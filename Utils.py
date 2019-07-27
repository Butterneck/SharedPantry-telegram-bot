import gzip
from sh import pg_dump
import globalVariables as gv
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError

class terminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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

def dropboxUpload(LOCALFILE):
    BACKUPPATH = '/backup.gz'
    dbx = dropbox.Dropbox(os.environ["DROPBOX_API_KEY"])

    try:
        dbx.users_get_current_account()
    except AuthError:
        print("ERROR: Invalid access TOKEN")
        return

    with open(LOCALFILE, 'rb') as f:
        print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
            print("Backup succeded!")
        except ApiError as err:
            if (err.error.is_path() and err.error.get_path().reason.is_insufficient_space()):
                print("Spazio insufficiente, impossibile eseguire il backup")
                return
            elif err.user_message_text:
                print(err.user_message_text)
                return
            else:
                print(err)
                return

def dbBackup():
    user = gv.DB_URL[11:25]
    password = gv.DB_URL[26:90]
    host = gv.DB_URL[91:138]
    port = gv.DB_URL[139:143]
    db = gv.DB_URL[144:]

    os.environ["PGPASSWORD"] = password

    with gzip.open('backup.gz', 'wb') as f:
        pg_dump('-h', host, '-U', user, db, '-p', port, _out=f)

    dropboxUpload(str(f))
