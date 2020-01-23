import connexion, json
from redis import StrictRedis
import os

class ExpenseApp(object):

    def __init__(self):
        redisHostname = os.environ.get('redisHost', 'localhost')
        print("Redis hostname: " + redisHostname)        
        self._rdb = StrictRedis(host=redisHostname, port=6379, db=0, socket_connect_timeout=2, socket_timeout=2)
        redisInfo = self._rdb.info()
        print("Redis version: " + redisInfo.get('redis_version'))
        print("Redis mode: " + redisInfo.get('redis_mode'))


    def add_expense(self, expense):           
        expense_key = self._rdb.incr('expense_key')             
        if not 'tags' in expense:
            expense.update({'tags': []})
        redis_key = 'id_' + str(expense_key)
        expense['id'] = redis_key
        self._rdb.set(redis_key, json.dumps(expense))
        expense_date = expense['date']    
        self._rdb.sadd(expense_date, redis_key)    
        return expense

    def get_expense_by_id(self, expenseId):                
        expense = self._rdb.get(expenseId)
        if expense is None:
            return 'Not Found', 404
        return json.loads(expense)

    def update_expense(self, expenseId, expense):
        if self._rdb.exists(expenseId):
            self._rdb.set(expenseId, json.dumps(expense))
        else:
            return 'Not Found', 404
        return expense

    def delete_expense(self, expenseId):
        if self._rdb.exists(expenseId):
            expense = json.loads(self._rdb.get(expenseId))
            expense_date = expense['date']
            self._rdb.delete(expenseId)            
            self._rdb.srem(expense_date, expenseId)
        else:
            return 'Not Found', 404
        return 'Deleted', 200

    def find_expenses_by_date(self, date):
        expenses_for_date = []    
        for expense_key in self._rdb.smembers(date):
            expenses_for_date.append(json.loads(self._rdb.get(expense_key)))
        return expenses_for_date

    def find_expenses_by_tags(self, tags = None):            
        expenses_list = []
        for expense_key in self._rdb.scan_iter(match='id_?'):        
            expenses_list.append(json.loads(self._rdb.get(expense_key)))
        if not tags:        
            return expenses_list
        else:
            filtered_list = []
            for expense in expenses_list:
                if all(elem in expense['tags'] for elem in tags):
                    filtered_list.append(expense)
            return filtered_list        

    def get_monthly_expenses(self, year_month):
        monthly_key_collection = set()
        for expense_dates in self._rdb.scan_iter(match= year_month + "-*"):
            monthly_key_collection.update(self._rdb.smembers(expense_dates))
        sum = 0
        monthlyExpenses = []
        for expense_key in monthly_key_collection:
            expense = json.loads(self._rdb.get(expense_key))
            sum = sum + expense['value']
            monthlyExpenses.append(expense)
        return {"year_month": year_month, "sum": sum, "expenses": monthlyExpenses}