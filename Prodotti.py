class Product():
    def __init__(self, id, name, price, qt):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = qt

    def __str__(self):
        return "[" + str(self.id) + "] " + self.name + "-" + str(self.quantity) + "-" + str(self.price)