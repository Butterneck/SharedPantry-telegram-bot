import globalVariables as gv

class Activator():
    def __init__(self, activator):
        self.activator = activator

        def run(self):
            gv.db_manager.checkActivator()
