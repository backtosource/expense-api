
import connexion
from appFunctions import expenses

functions = expenses.Expenses()

def add_expense(expense):    
    return functions.add_expense(expense)

def get_expense_by_id(expenseId):    
    return functions.get_expense_by_id(expenseId)

def update_expense(expense):    
    return functions.update_expense(expense)

def delete_expense(expenseId):    
    return functions.delete_expense(expenseId)

def find_expenses_by_date(date):
    return functions.find_expenses_by_date(date)

def find_expenses_by_tags(tags=[]):        
    return functions.find_expenses_by_tags(tags)

def get_monthly_expenses(month):        
    return functions.get_monthly_expenses(month)