#!/usr/bin/env python3

from __future__ import unicode_literals
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import print_formatted_text, HTML
import datetime
from functools import reduce

import Utils
from url_getter import get_pg_url_from_heroku
from db_connection_postgresql import *


command_completer = WordCompleter(['help',
                                   'list_products',
                                   'list_users',
                                   'list_transactions'], ignore_case=True)

def print_products(products):
    generated_string = "Prodotti"
    for product in products:
        generated_string += "\n" + str(product.id) + " " + product.name + " " + str(product.price) + "€" + " " + str(product.quantity)
    print_formatted_text(generated_string)

def list_products(db_manager, args=[]):
    if len(args) == 0:
        #Mostro tutti i prodotti
        print_products(db_manager.getAllProduct())
    elif args[0] == '-a':
        pass


def print_users(users):
    generated_string = "Utenti"
    for user in users:
        generated_string += "\n" + str(user.id) + " " + user.nome + " " + str(user.chat_id)
    print_formatted_text(generated_string)

def list_users(db_manager, args=[]):
    if len(args) == 0:
        #Mostro tutti gli utenti
        print_users(db_manager.getAllusers())

def print_transactions(transactions, users, products):
    generated_string = "Transazioni"
    for transaction in transactions:
        user = list(filter(lambda u: u.id == transaction.user_id, users))[0]
        product = list(filter(lambda p: p.id == transaction.product_id, products))[0]
        generated_string += "\n" + str(transaction.id) + " " + str(transaction.date) + " " + str(transaction.quantity) + " " + user.nome + " " + product.name
    print_formatted_text(generated_string)

def list_transactions(db_manager, args=[]):
    if len(args) == 0:
        print_transactions(db_manager.getAllDebits(), db_manager.getAllusers(), db_manager.getAllProduct())

def handle_cmd(cmd, db_manager):
    if cmd == 'help':
        print("--HELP--")
    elif cmd == 'list_products':
        list_products(db_manager, [])
    elif cmd == 'list_users':
        list_users(db_manager, [])
    elif cmd == 'list_transactions':
        list_transactions(db_manager, [])

def main():
    session = PromptSession(completer=command_completer,
                            complete_while_typing=True,
                            history=FileHistory('.manage_history'),
                            auto_suggest=AutoSuggestFromHistory())

    heroku_mail = session.prompt("Heroku email: ")
    heroku_password = session.prompt("Heroku password: ", is_password=True)
    heroku_prject_name = session.prompt("Heroku prject name: ", is_password=False)

    path_to_geckodriver = "/Users/marco/Downloads/geckodriver"

    pg_url = get_pg_url_from_heroku(heroku_mail, heroku_password, heroku_prject_name, path_to_geckodriver, 2)
    db_manager = DB_Connection(pg_url)

    while True:
        try:
            text = session.prompt("> ")
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            handle_cmd(text, db_manager)
    print("Closing")

if __name__ == '__main__':
    main()