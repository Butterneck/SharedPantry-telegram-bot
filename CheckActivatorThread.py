from threading import Thread
import globalVariables as gv
from contabilita import Wallet
import time

class CheckActivatorThread(Thread):
    def __init__(self, bot, db_manager):
        '''Constructor'''
        Thread.__init__(self)
        self.bot = bot
        self.db_manager = db_manager

    def run(self):
        while True:
            if self.db_manager.checkActivator():  # Check the value of activator
                Wallet.sedDebitoMensile(self.bot)
                self.db_manager.deactivateActivator() # reset activator value
                return
            time.sleep(3)
