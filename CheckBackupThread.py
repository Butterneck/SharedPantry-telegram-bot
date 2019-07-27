from threading import Thread
import globalVariables as gv
import time
from Utils import dbBackup, dropboxUpload, removeOldBackups

class CheckBackupThread(Thread):
    def __init__(self):
        '''Constructor'''
        Thread.__init__(self)

    def run(self):
        while True:
            if gv.db_manager.checkBackup():
                dbBackup()
                gv.db_manager.deactivateBackup()
                return
            time.sleep(3)
