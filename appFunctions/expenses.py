import datetime

class Expenses(object):

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
        return [expense for expense in list(self.EXPENSES.values()) if date == expense['date']]

    def find_expenses_by_tags(self, tags=[]):        
        if not tags:
            return list(self.EXPENSES.values())
        else:
            return [expense for expense in list(self.EXPENSES.values()) if set(tags).issubset(expense['tags'])]        

    def get_monthly_expenses(self, month):        
        monthlyExpenses = [expense for expense in list(self.EXPENSES.values()) if datetime.datetime.strptime(expense['date'], "%Y-%m-%d").date().month == month]
        sum = 0
        for expense in monthlyExpenses:
            sum = sum + expense['value']
        return {"month": month, "sum": sum, "expenses": monthlyExpenses}