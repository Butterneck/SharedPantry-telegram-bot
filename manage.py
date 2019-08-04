#!/usr/bin/env python3

from __future__ import unicode_literals
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.shortcuts import input_dialog, radiolist_dialog, yes_no_dialog
from sys import exit, argv
import urllib3
from os import environ, path

import Utils
import datetime
from url_getter import get_pg_url_from_heroku
from geckodriver_getter import get_geckodriver_binary
from db_connection_postgresql import *

command_completer = WordCompleter(['help',
                                   'list_products',
                                   'list_users',
                                   'list_transactions',
                                   'insert_new_user',
                                   'insert_new_product',
                                   'insert_new_transaction',
                                   'remove_product',
                                   'remove_user',
                                   'remove_transaction',
                                   'modify_quantity',
                                   'drop_all_tables',
                                   'trigger_backup',
                                   'trigger_send_conto',
                                   'run_query'], ignore_case=True)


def get_path_to_geckodriver(session):
    if 'GECKODRIVER_PATH' not in environ:
        path_to_geckodriver = session.prompt("Path to geckodriver file (empty to download it): ")
        if path_to_geckodriver == "":
            # Dowload geckodriver in ./geckdriver
            print(terminalColors.ITALIC + "Download geckodriver in this directory" + terminalColors.ENDC)
            print(terminalColors.WARNING + "You need also Firefox to get postgresql databse url from Heroku" + terminalColors.ENDC)
            path_to_geckodriver = "./geckodriver"

        if not get_geckodriver_binary(path_to_geckodriver):
            print(terminalColors.FAIL + "Daownload of geckodriver failed" + terminalColors.ENDC)
            exit(1)

        url_file = open(".path_to_geckodriver", "w+")
        url_file.write(path_to_geckodriver)
        url_file.close()
        print("Path salvata in .path_to_geckodriver")
        return path_to_geckodriver
    else:
        return environ['GECKODRIVER_PATH']


def get_pg_url(session):
    heroku_mail = session.prompt("Heroku email: ")
    heroku_password = session.prompt("Heroku password: ", is_password=True)
    heroku_prject_name = session.prompt("Heroku project name: ", is_password=False)
    heroku_project_index = int(session.prompt("Heroku project index (in dashboard) (index starts from 0): "))

    path_to_geckodriver = get_path_to_geckodriver(session)

    try:
        pg_url = get_pg_url_from_heroku(heroku_mail, heroku_password, heroku_prject_name, path_to_geckodriver,
                                        heroku_project_index)
        url_file = open(".postgres_url_cached", "w+")
        url_file.write(pg_url)
        url_file.close()
        print("Url salvato in .postgres_url_cached")
        return pg_url
    except:
        print(terminalColors.FAIL + "Impossibile trovare l'url al DB postgres su Heroku" + terminalColors.ENDC)
        print(terminalColors.WARNING + "[-]Controllare la variabile 'path_to_geckodriver' in manage.py")
        print("[-]Deve essere installato Firefox e il file geckodriver presente alla path indicata")
        print("[-]Per maggiori info o dubbi aprire una issue su gitlab" + terminalColors.ENDC)
        print(terminalColors.FAIL + "Quitting" + terminalColors.ENDC)
        exit(1)

def get_db_connection(session):
    name_DB = "Manage_DB"
    if 'PG_URL_MANAGE' in environ:
        print("Url slavato in precedenza")
        try:
            db_connection = DB_Connection(environ['PG_URL_MANAGE'], name_DB)
        except:
            print("URL non valido, tetativo di ricezione nuovo url")
            db_connection = DB_Connection(get_pg_url(session), name_DB)
    else:
        db_connection = DB_Connection(get_pg_url(session), name_DB)

    return db_connection


def print_products(products):
    generated_string = "Prodotti"
    for product in products:
        generated_string += "\n" + str(product.id) + " " + product.name + " " + str(product.price) + "€" + " " + str(
            product.quantity)
    print_formatted_text(generated_string)


def list_products(db_manager, args=[]):
    if len(args) == 0:
        # Mostro tutti i prodotti
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
        # Mostro tutti gli utenti
        print_users(db_manager.getAllusers())


def print_transactions(transactions, users, products):
    generated_string = "Transazioni"
    for transaction in transactions:
        user = list(filter(lambda u: u.id == transaction.user_id, users))[0]
        product = list(filter(lambda p: p.id == transaction.product_id, products))[0]
        generated_string += "\n" + str(transaction.id) + " " + str(transaction.date) + " " + str(
            transaction.quantity) + " " + user.nome + " " + product.name
    print_formatted_text(generated_string)


def list_transactions(db_manager, args=[]):
    if len(args) == 0:
        print_transactions(db_manager.getAllDebits(), db_manager.getAllusers(), db_manager.getAllProduct())


def insert_new_user(db_manager, args=[]):
    username = input_dialog(
        title='New user',
        text='Name:')
    if username is None:
        return None

    chat_id = input_dialog(
        title='New user',
        text='Chat_Id:')
    if chat_id is None:
        return None

    if db_manager.addUser(username, chat_id):
        print("Inserimento avvenuto con successo")
    else:
        print("Utente non inserito, errore")


def insert_new_product(db_manager, args=[]):
    name = input_dialog(
        title='New product',
        text='Name:'
    )
    if name is None:
        return None

    qt = input_dialog(
        title='New product',
        text='Quantity:'
    )
    if qt is None:
        return None

    price = input_dialog(
        title='New product',
        text='Price:'
    )
    if price is None:
        return None

    if db_manager.addProduct(name, price, qt):
        print("Inserimento avvenuto con successo")
    else:
        print("Prodotto non inserito, errore")


# restituisce la chat-id dell'utente selezionato
def user_chooice(users, title, text):
    if len(users) == 0:
        print("Users not found. Insert some users")
        return None

    users_list = []
    for user in users:
        u = (str(user.chat_id), user.nome)
        users_list.append(u)

    choose_user = radiolist_dialog(
        title=title,
        text=text,
        values=users_list
    )
    return choose_user


# restituisce il product-id del prodotto selezionato
def product_chooice(products, title, text):
    if len(products) == 0:
        print("Products not found. Insert some products")
        return None

    product_list = []

    for product in products:
        p = (str(product.id), product.name)
        product_list.append(p)

    choose_product = radiolist_dialog(
        title=title,
        text=text,
        values=product_list
    )

    return choose_product


# restituisce l'id della transazione selezionata
def transaction_chooice(transactions, products, title, text):
    if len(transactions) == 0:
        print("User without transactions")
        return None

    transactions_list = []
    for transaction in transactions:
        product_buought = [product for product in products if product.id == transaction.product_id][0]
        t = (
            str(transaction.id),
            str(transaction.date) + "-" + product_buought.name + " " + str(product_buought.quantity))
        transactions_list.append(t)

    chooice_transaction = int(radiolist_dialog(
        title=title,
        text=text,
        values=transactions_list
    ))

    return chooice_transaction


# richiesta quantità
def quantity_chooice(title, text):
    qt = int(input_dialog(
        title=title,
        text=text
    ))

    return qt


def insert_new_transaction(db_manager, args=[]):
    users = db_manager.getAllusers()
    products = db_manager.getAllProduct()

    # Scelta dell'utente che ha fatto l'acquisto
    choose_user = user_chooice(users, 'New transaction', 'User')
    if choose_user is None:
        return None

    # Scelta del prodotto acqusitato
    choose_product = product_chooice(products, 'New transaction', 'Product')
    if choose_product is None:
        return None

    qt = quantity_chooice('New transaction', 'Quantity bought:')
    if qt is None:
        return None

    if db_manager.addTransaction(choose_user, choose_product, qt):
        print("Inserimento avvenuto con successo")
    else:
        print("Transazione non inserita, errore")


def remove_product(db_manager, args=[]):
    print("Not yet implemented")


def remove_user(db_manager, args=[]):
    print("Not yet implemented")


def remove_transaction(db_manager, args=[]):
    user_chat_id = user_chooice(db_manager.getAllusers(), "Remove transaction", "User")
    if user_chat_id is None:
        return None

    products = db_manager.getAllProduct()
    transactions = db_manager.getAllAcquisti(user_chat_id)
    transactions.sort(key=lambda a: a.id, reverse=True)
    transaction_id = transaction_chooice(transactions, products, "Remove transaction", "Transaction")
    if transaction_id is None:
        return None
    transaction = [t for t in transactions if int(transaction_id) == t.id][0]

    db_manager.removeTransaction(transaction_id)
    result = yes_no_dialog(
        title="Remove transaction",
        text="Add removed transaction quantity to dispensa?"
    )
    if result:
        product = [p for p in products if int(p.id) == int(transaction.product_id)][0]
        new_quantity = product.quantity + transaction.quantity
        if db_manager.modifyQuantity(product.id, new_quantity):
            print("Modifica avvenuta con successo")
        else:
            print("Modifica non avvenuta, errore")


def modify_quantity(db_manager, args=[]):
    products = db_manager.getAllProduct()

    product_to_modify_id = product_chooice(products, "Modify product", "Product")
    if product_to_modify_id is None:
        return None

    modified_quantity = quantity_chooice("Modify product", "Quantity modified (+/-)")
    if modified_quantity is None:
        return None

    last_quantity = [product for product in products if int(product.id) == int(product_to_modify_id)][0].quantity
    new_quantity = last_quantity + modified_quantity
    if db_manager.modifyQuantity(product_to_modify_id, new_quantity):
        print("Modifica avvenuta con successo")
    else:
        print("Modifica non avvenuta, errore")


def drop_all_tables(db_manager, args=[]):
    result = yes_no_dialog(
        title="Dropping all tables",
        text="All data will be lost.\nYou are working on " + db_manager.path + "\n Are you sure?"
    )
    if result:
        db_manager.dropAllTables()


def trigger_backup(db_manager, args=[]):
    url_trigger_backup = "https://backuptrigger.herokuapp.com/"
    http = urllib3.PoolManager()
    r = http.request('GET', url_trigger_backup)
    print(r.status)


def trigger_send_conto(db_manager, args=[]):
    if args[0] == '-r':
        print("Sending request to Heroku...")
        url_trigger_send_conto = "https://cianobotactivator.herokuapp.com/"
        http = urllib3.PoolManager()
        r = http.request('GET', url_trigger_send_conto)
        print(r.status)


def run_query(db_manager, args=[]):
    if len(args) == 0:
        query = prompt("sql: ")
        result = db_manager.runSqlQuery(query)
        if result:
            print(result)


def print_help():
    print(terminalColors.BOLD + 'Cianobot manage utility help' + terminalColors.ENDC)
    print(terminalColors.UNDERLINE + 'Launch:' + terminalColors.ENDC)

    print_formatted_text(HTML('./manage.py'))
    print('\tLaunch this utility')

    print('./manage.py --new-pg-url')
    print('\tLaunch this utility and change the cached postgresql database url saved in .postgrers_url_cached file')

    print('./manage.py --help')
    print('\tShow this help')

    print('')

    print(terminalColors.UNDERLINE + 'Commands:' + terminalColors.ENDC)

    print('[*]' + terminalColors.UNDERLINE + 'Lists:' + terminalColors.ENDC)

    print('\tlist_products')
    print("\t\tPrint all products")

    print('\tlist_users')
    print("\t\tPrint all users")

    print('\tlist_transactions')
    print("\t\tPrint all transactions")

    print('[*]' + terminalColors.UNDERLINE + 'Insert:' + terminalColors.ENDC)

    print('\tinsert_new_product')
    print("\t\tInsert a new product")

    print('\tinsert_new_user')
    print("\t\tInsert a new user")

    print('\tinsert_new_transaction')
    print("\t\tInsert a new transaction")

    print('[*]' + terminalColors.UNDERLINE + 'Remove:' + terminalColors.ENDC)

    print('\tremove_product')
    print("\t\t" + terminalColors.ITALIC + "Not implemented yet" + terminalColors.ENDC + " Remove a product")

    print('\tremove_user')
    print("\t\t" + terminalColors.ITALIC+ "Not implemented yet" + terminalColors.ENDC + " Remove a user")

    print('\tremove_transaction')
    print("\t\tRemove a transaction")

    print('[*]' + terminalColors.UNDERLINE + 'Trigger:' + terminalColors.ENDC)

    print('\ttrigger_backup')
    print("\t\t" + terminalColors.ITALIC + "Not working" + terminalColors.ENDC + " Trigger the backup process")

    print('\ttrigger_send_conto')
    print("\t\t" + terminalColors.ITALIC + "Not working" + terminalColors.ENDC + " Trigger the send monthly message process")

    print('[*]' + terminalColors.UNDERLINE + 'Others:' + terminalColors.ENDC)

    print('\tmodify_quantity')
    print("\t\tModify the quantity of a product")

    print('\tdrop_all_tables')
    print("\t\t" + terminalColors.BOLD + "Warning - dangerous operation" + terminalColors.ENDC + " Delete all data from database")

    print('\trun_query')
    print("\t\t" + terminalColors.BOLD + "Warning - dangerous operation" + terminalColors.ENDC + " Run an arbitrary query in databse")


def handle_cmd(cmd, db_manager):
    args = cmd.split(' ')
    cmd = args.pop(0)
    if cmd == 'help':
        print_help()
    elif cmd == 'list_products':
        list_products(db_manager, args)
    elif cmd == 'list_users':
        list_users(db_manager, args)
    elif cmd == 'list_transactions':
        list_transactions(db_manager, args)
    elif cmd == 'insert_new_user':
        insert_new_user(db_manager, args)
    elif cmd == 'insert_new_product':
        insert_new_product(db_manager, args)
    elif cmd == 'insert_new_transaction':
        insert_new_transaction(db_manager, args)
    elif cmd == 'remove_product':
        remove_product(db_manager, args)
    elif cmd == 'remove_user':
        remove_user(db_manager, args)
    elif cmd == 'remove_transaction':
        remove_transaction(db_manager, args)
    elif cmd == 'modify_quantity':
        modify_quantity(db_manager, args)
    elif cmd == 'drop_all_tables':
        drop_all_tables(db_manager, args)
    elif cmd == 'trigger_backup':
        trigger_backup(db_manager, args)
    elif cmd == 'trigger_send_conto':
        trigger_send_conto(db_manager, args)
    elif cmd == 'run_query':
        run_query(db_manager, args)


def main():
    session = PromptSession(completer=command_completer,
                            complete_while_typing=True,
                            history=FileHistory('.manage_history'),
                            auto_suggest=AutoSuggestFromHistory())

    if path.exists(".postgres_url_cached"):
        environ['PG_URL_MANAGE'] = open(".postgres_url_cached", "r").read()

    if path.exists(".path_to_geckodriver"):
        environ['GECKODRIVER_PATH'] = open(".path_to_geckodriver", "r").read()

    if len(argv) == 1:
        db_manager = get_db_connection(session)
    elif argv[1] == '--new-pg-url':
        db_manager = DB_Connection(get_pg_url(session))
    elif argv[1] == '--help':
        print_help()
        return

    print(terminalColors.HEADER + "Welcome, write help to see what this utility can do" + terminalColors.ENDC)
    while True:
        try:
            text = session.prompt("> ", validator=None)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            handle_cmd(text, db_manager)


if __name__ == '__main__':
    main()
