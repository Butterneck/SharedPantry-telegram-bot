from threading import Thread
import globalVariables as gv
from contabilita import debitoMensile
import time

class MyThread(Thread):
    def __init__(self):
        '''Constructor'''
        Thread.__init__(self)

    def run(self):
        while True:
            if gv.db_manager.checkActivator():  # Check the value of activator
                debitoMensile()
                gv.db_manager.deactivateActivator() # reset activator value
                return
            time.sleep(3000)
