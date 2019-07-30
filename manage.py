#!/usr/bin/env python3

from __future__ import unicode_literals
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

import globalVariables as gv


command_completer = WordCompleter(['help',
                                   'list_products',
                                   'list_users',
                                   'list_transactions'], ignore_case=True)

def list_products(args=[]):
    if len(args) == 0:
        #Mostro tutti i prodotti
        pass
    elif args[0] == '-a':
        pass
def handle_cmd(cmd):
    if cmd == 'help':
        print("--HELP--")
    elif cmd == 'list_products':
        print("Prodotti")
    elif cmd == 'list_users':
        print("Utenti")
    elif cmd == 'list_transactions':
        print("Transazioni")

def main():
    session = PromptSession(completer=command_completer,
                            complete_while_typing=True,
                            history=FileHistory('.manage_history'),
                            auto_suggest=AutoSuggestFromHistory())
    heroku_mail = session.prompt("Heroku email: ")
    heroku_password = session.prompt("Heroku password: ", is_password=True)

    while True:
        try:
            text = session.prompt("> ")
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            handle_cmd(text)
    print("Closing")

if __name__ == '__main__':
    main()