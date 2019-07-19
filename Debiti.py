class Debit():
    def __init__(self, id, user_id, quantity, month):
        self.id = id
        self.user_id = user_id
        self.quantity = quantity
        self.month = month
        self.paid = 0
