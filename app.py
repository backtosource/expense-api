import connexion, datetime

EXPENSES = {}
runnung_id = 0

# Needed for testing only
def resetApp():
    global EXPENSES
    EXPENSES.clear()
    global runnung_id
    runnung_id = 0

def add_expense(expense):    
    global EXPENSES
    global runnung_id
    runnung_id = runnung_id + 1
    expense['id'] = runnung_id
    if not 'tags' in expense:
        expense.update({'tags': []})
    EXPENSES.update({runnung_id : expense})
    return expense

def get_expense_by_id(expenseId):
    global EXPENSES
    try:
        expense = EXPENSES[expenseId]
    except KeyError as e:
        return 'Not Found', 404
    return expense

def update_expense(expenseId, expense):
    global EXPENSES
    try:    
        EXPENSES[expenseId] = expense
    except KeyError as e:
        return 'Not Found', 404
    return EXPENSES[expenseId]

def delete_expense(expenseId):
    global EXPENSES
    try:
        EXPENSES.pop(expenseId)
    except KeyError as e:
        return 'Not Found', 404
    return None

def find_expenses_by_date(date):
    global EXPENSES
    return [expense for expense in list(EXPENSES.values()) if date == expense['date']]

def find_expenses_by_tags(tags=[]):
    global EXPENSES        
    if not tags:
        return list(EXPENSES.values())
    else:
        return [expense for expense in list(EXPENSES.values()) if set(tags).issubset(expense['tags'])]        

def get_monthly_expenses(month):
    global EXPENSES        
    monthlyExpenses = [expense for expense in list(EXPENSES.values()) if datetime.datetime.strptime(expense['date'], "%Y-%m-%d").date().month == month]
    sum = 0
    for expense in monthlyExpenses:
        sum = sum + expense['value']
    return {"month": month, "sum": sum, "expenses": monthlyExpenses}