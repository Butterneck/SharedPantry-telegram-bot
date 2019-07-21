import globalVariables as gv

class Activator():
    def __init__(self, activator):
        self.activator = activator

    def run(self):
        while True:
            if gv.db_manager.checkActivator():  # Check the value of activator
                debitoMensile(self.bot)
                gv.db_manager.deactivateActivator() # reset activator value
            print('sono qui')
            time.sleep(3)
