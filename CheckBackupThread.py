from threading import Thread
import globalVariables as gv
import time
from Utils import dbBackup, dropboxUpload, removeOldBackups

class CheckBackupThread(Thread):
    def __init__(self, db_manager):
        '''Constructor'''
        Thread.__init__(self)
        self.db_manager = db_manager

    def run(self):
        while True:
            if gv.db_manager.checkBackup():
                dbBackup()
                self.db_manager.deactivateBackup()
                return
            time.sleep(3)
