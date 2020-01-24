class Month:
    def __init__(self, name, monthNum, days, previousMonth=None):
        self.name = name
        self.monthNum = monthNum
        self.days = days
        self.previousMonth = previousMonth

    def getPreviousMonth(self):
        return self.previousMonth

    def getNumDays(self):
        return self.days

    def getNumMonth(self):
        return self.monthNum

    def getName(self):
        return self.name


class Year:
    year = []

    def __init__(self):
        self.year.append(Month('January', 1, 31))
        self.year.append(Month('February', 2, 28, self.year[len(self.year) - 1]))
        self.year.append(Month('March', 3, 31, self.year[len(self.year) - 1]))
        self.year.append(Month('April', 4, 30, self.year[len(self.year) - 1]))
        self.year.append(Month('May', 5, 31, self.year[len(self.year) - 1]))
        self.year.append(Month('June', 6, 30, self.year[len(self.year) - 1]))
        self.year.append(Month('July', 7, 31, self.year[len(self.year) - 1]))
        self.year.append(Month('August', 8, 31, self.year[len(self.year) - 1]))
        self.year.append(Month('September', 9, 30, self.year[len(self.year) - 1]))
        self.year.append(Month('October', 10, 31, self.year[len(self.year) - 1]))
        self.year.append(Month('November', 11, 30, self.year[len(self.year) - 1]))
        self.year.append(Month('December', 12, 31, self.year[len(self.year) - 1]))
        # Closing circular list
        self.year[0].previousMonth = self.year[len(self.year) - 1]
