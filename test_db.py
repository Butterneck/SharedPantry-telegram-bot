import pytest
import globalVariables as gv
import datetime
from db_connection_postgresql import DB_Connection
import globalVariables as gv

'''
In caso di fallimento dei test:
    * Aggiornare l'URL per l'istaziazione di db_manager_for_test
'''
db_manager_for_test = DB_Connection(DB_URL="postgres://ixiqvhfvwxoesq:7a7c7c6514e38c66bf3c730cee009fba2f1f4b2ebe9fd92bf100c84764312ece@ec2-176-34-184-174.eu-west-1.compute.amazonaws.com:5432/dfip2e6s7bg4ik", sslRequired=True, db_name="Test_DB")


user_data = [("Marco", 1),
             ("Filippo", 2),
             ("Scanta", 3),
             ("Mase", 4),
             ("Ciano", 34),
             ("Gul", 78),
             ("Marco_Admin", 179624122)]

product_data = [("Breh", 0.5, 10),
                ("Fonzi", 0.25, 25),
                ("Snica", 1.2, 30)]

transaction_data = [(1, 1, 1),
                    (2, 2, 2),
                    (3, 3, 1),
                    (3, 2, 2),
                    (34, 2, 1),
                    (78, 1, 1),
                    (2, 1, 1),
                    (4, 2, 1),
                    (1, 3, 1),
                    (1, 3, 2)]

user_retrieved = []
transaction_retrieved = []
product_retrieved = []


class Test_db(object):

    def test_dropAllTables_start(self):
        print("Dropping data to begin automatic tests")
        db_manager_for_test.cleanCursor()
        assert db_manager_for_test.dropAllTables()

    def test_addUser(self):
        db_manager_for_test.cleanCursor()
        users_added = []
        for user in user_data:
            users_added.append(db_manager_for_test.addUser(user[0], user[1]))
        assert len(users_added) == 7

    def test_getChatIds(self):
        db_manager_for_test.cleanCursor()
        chat_ids = db_manager_for_test.getAllChatIds()
        users_chat_ids = list(map(lambda u: u[1], user_data))
        assert chat_ids == users_chat_ids

    def test_addProduct(self):
        db_manager_for_test.cleanCursor()
        product_added = []
        for product in product_data:
            product_added.append(db_manager_for_test.addProduct(product[0], product[1], product[2]))
        assert len(product_added) == 3

    def test_addTransaction(self):
        db_manager_for_test.cleanCursor()
        transaction_added = []
        for transaction in transaction_data:
            transaction_added.append(db_manager_for_test.addTransaction(transaction[0], transaction[1], transaction[2]))
        assert len(transaction_added) == 10

    def test_getAllusers(self):
        db_manager_for_test.cleanCursor()
        user_retrieved = db_manager_for_test.getAllusers()
        assert len(user_retrieved) == len(user_retrieved)

    def test_getAllTransaction(self):
        db_manager_for_test.cleanCursor()
        transaction_retrieved = db_manager_for_test.getAllDebits()
        assert len(transaction_retrieved) == len(transaction_data)

    def test_getAllProduct(self):
        db_manager_for_test.cleanCursor()
        product_retrieved = db_manager_for_test.getAllProduct()
        assert len(product_retrieved) == len(product_data)

    def test_getUsername_fromChatId(self):
        userNames = []
        for user in user_data:
            userNames.append(db_manager_for_test.getUsername_fromChatId(user[1]))
        assert userNames == list(map(lambda u: u[0], user_data))


    def test_getAllAcquisti(self):
        test = True
        for user in user_data:
            acqusti_for_user_getted = db_manager_for_test.getAllAcquisti(user[1])
            print("getted",len(acqusti_for_user_getted))
            acqusti_for_user = list(filter(lambda a: a[0] == user[1], transaction_data))
            print("base", len(acqusti_for_user))
            test = test and (len(acqusti_for_user) == len(acqusti_for_user_getted))
        assert test

    def test_removeTransaction(self):
        db_manager_for_test.cleanCursor()
        removed_transaction = []
        for tr in transaction_retrieved:
            removed_transaction.append(db_manager_for_test.removeTransaction(tr.id))
        t: bool
        for t in removed_transaction:
            assert t

    def test_removeProduct(self):
        db_manager_for_test.cleanCursor()
        removed_product = []
        for pr in product_retrieved:
            removed_product.append(db_manager_for_test.removeProduct(pr.id))

        p: bool
        for p in removed_product:
            assert p

    def test_removeUser(self):
        db_manager_for_test.cleanCursor()
        removed_user = []
        for user in user_retrieved:
            removed_user.append(db_manager_for_test.removeUser(user.chat_id))

        u: bool
        for u in removed_user:
            assert u

    def test_activateActivator(self):
        db_manager_for_test.cleanCursor()
        db_manager_for_test.activateActivator()
        assert db_manager_for_test.checkActivator() == True

    def test_deactivateActivator(self):
        db_manager_for_test.cleanCursor()
        db_manager_for_test.deactivateActivator()
        assert db_manager_for_test.checkActivator() == False

    def test_dropAllTables_end(self):
        print("Dropping data to clean DB")
        db_manager_for_test.cleanCursor()
        assert db_manager_for_test.dropAllTables()
