class Authenticator():
    Ciano = 879140791  # Ciano
    Filippo = 32345162  # Filippo
    Marco = 179624122  # Marco
    admin_ids = [Filippo]

    def checkAuthentication(self, update):
        if update.message.chat_id not in self.admin_ids:
            print("Utente " + str(update.message.chat_id) + " non registrato")
            return False
        else:
            return True
