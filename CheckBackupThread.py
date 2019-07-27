from threading import Thread
import globalVariables as gv
import time
from Utils import dbBackup dropboxUpload

class CHeckBackupThread(Thread):
    def __init__(self):
        '''Constructor'''
        Thread.__init__(self)

    def run(self):
        for i in range(200):
            if gv.db_manager.checkBackup():
                dbBackup()
                gv.db_manager.deactivateBackup()
                return
            time.sleep(3)
