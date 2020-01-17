from model.ExpenseApp import ExpenseApp

expense_app = ExpenseApp()

def add_expense(expense):          
    return expense_app.add_expense(expense)

def get_expense_by_id(expenseId):        
    return expense_app.get_expense_by_id(expenseId)

def update_expense(expenseId, expense):
    return expense_app.update_expense(expenseId, expense)

def delete_expense(expenseId):            
    return expense_app.delete_expense(expenseId)

def find_expenses_by_date(date):
    return expense_app.find_expenses_by_date(date)

def find_expenses_by_tags(tags=[]):            
    return expense_app.find_expenses_by_tags(tags)

def get_monthly_expenses(year_month):
    return expense_app.get_monthly_expenses(year_month)