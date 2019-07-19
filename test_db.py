import pytest
import globalVariables as gv
import datetime

user_data = [("Marco", 1),
             ("Filippo", 2),
             ("Scanta", 3),
             ("Mase", 4),
             ("Ciano", 34),
             ("Gul", 78)]

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

    def test_dropAllTables(self):
        gv.db_manager_for_test.cleanCursor()
        assert gv.db_manager_for_test.dropAllTables()

    def test_addUser(self):
        gv.db_manager_for_test.cleanCursor()
        users_added = []
        for user in user_data:
            users_added.append(gv.db_manager_for_test.addUser(user[0], user[1]))
        assert len(users_added) == 6

    def test_getChatIds(self):
        gv.db_manager_for_test.cleanCursor()
        chat_ids = gv.db_manager_for_test.getAllChatIds()
        users_chat_ids = list(map(lambda u: u[1], user_data))
        assert chat_ids == users_chat_ids

    def test_addProduct(self):
        gv.db_manager_for_test.cleanCursor()
        product_added = []
        for product in product_data:
            product_added.append(gv.db_manager_for_test.addProduct(product[0], product[1], product[2]))
        assert len(product_added) == 3

    def test_addTransaction(self):
        gv.db_manager_for_test.cleanCursor()
        transaction_added = []
        for transaction in transaction_data:
            transaction_added.append(gv.db_manager_for_test.addTransaction(transaction[0], transaction[1], transaction[2]))
        assert len(transaction_added) == 10

    def test_getAllusers(self):
        gv.db_manager_for_test.cleanCursor()
        user_retrieved = gv.db_manager_for_test.getAllusers()
        assert len(user_retrieved) == len(user_retrieved)

    def test_getAllTransaction(self):
        gv.db_manager_for_test.cleanCursor()
        transaction_retrieved = gv.db_manager_for_test.getAllDebits()
        assert len(transaction_retrieved) == len(transaction_data)

    def test_getAllProduct(self):
        gv.db_manager_for_test.cleanCursor()
        product_retrieved = gv.db_manager_for_test.getAllProduct()
        assert len(product_retrieved) == len(product_data)

    def test_removeTransaction(self):
        gv.db_manager_for_test.cleanCursor()
        removed_transaction = []
        for tr in transaction_retrieved:
            removed_transaction.append(gv.db_manager_for_test.removeTransaction(tr.id))
        t: bool
        for t in removed_transaction:
            assert t

    def test_removeProduct(self):
        gv.db_manager_for_test.cleanCursor()
        removed_product = []
        for pr in product_retrieved:
            removed_product.append(gv.db_manager_for_test.removeProduct(pr.id))

        p: bool
        for p in removed_product:
            assert p


    def test_removeUser(self):
        gv.db_manager_for_test.cleanCursor()
        removed_user = []
        for user in user_retrieved:
            removed_user.append(gv.db_manager_for_test.removeUser(user.chat_id))

        u: bool
        for u in removed_user:
            assert u

    def test_activateActivator(self):
        gv.db_manager.cleanCursor()
        gv.db_manager_for_test.activateActivator()
        assert gv.db_manager_for_test.checkActivator() == True

    def test_deactivateActivator(self):
        gv.db_manager_for_test.cleanCursor()
        gv.db_manager_for_test.deactivateActivator()
        assert gv.db_manager_for_test.checkActivator() == False
