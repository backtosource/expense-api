import connexion

class AppFunctions(object):

    def __init__(self):
        self.EXPENSES = {}

    def add_expense(self, expense):
        currentLength = len(self.EXPENSES)
        newId = currentLength + 1
        expense['id'] = newId
        self.EXPENSES[newId] = expense
        return expense

    def get_expense_by_id(self, expenseId):
        expense = self.EXPENSES[expenseId]
        return expense

    def update_expense(self, expense):
        expenseId = expense['id']
        self.EXPENSES[expenseId] = expense
        return self.EXPENSES[expenseId]

    def delete_expense(self, expenseId):
        self.EXPENSES.pop(expenseId)
        return None

    def find_expenses_by_date(self, date):
        return None

    def find_expenses_by_tags(self, tags):
        if not tags:
            return list(self.EXPENSES.values())
        else:
            return []
        

    def get_monthly_expenses(self, month):
        return None