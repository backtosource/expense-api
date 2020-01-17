from model.ExpenseApp import ExpenseApp
from unittest import TestCase
from unittest.mock import patch
import json

class TestRESTApp(TestCase):   

    _testExpense = {"value" : 1.2, "desc" : "Bread", "date" : "2019-10-01", "tags" : ["food"]}
    _testExpenseNew = {"value" : 1.2, "desc" : "Bread", "date" : "2019-10-01", "id" : 1, "tags" : ["food"]}
    _testExpenseUpdate = {"value" : 1.2, "desc" : "Toast", "date" : "2019-10-01", "id" : 1, "tags" : ["food", "daily"]}
    _testExpenseDate2 = {"value" : 2.5, "desc" : "Apples", "date" : "2019-10-10", "tags" : ["food"]}
 
    @patch('model.ExpenseApp.Redis.incr', return_value = 1)
    @patch('model.ExpenseApp.Redis.set')
    @patch('model.ExpenseApp.Redis.sadd')
    def test_add_expense(self, mock_redis_incr, mock_redis_set, mock_redis_sadd):
        app = ExpenseApp()                      
        self.assertEqual(app.add_expense(TestRESTApp._testExpense), TestRESTApp._testExpenseNew)
        mock_redis_incr.assert_called_once()
        mock_redis_set.assert_called_once()
        mock_redis_sadd.assert_called_once()

    @patch('model.ExpenseApp.Redis.get')
    def test_get_expense_by_id(self, mock_redis_get):
        app = ExpenseApp()
        mock_redis_get.return_value = json.dumps(TestRESTApp._testExpenseNew)
        self.assertEqual(app.get_expense_by_id(1), TestRESTApp._testExpenseNew)
        mock_redis_get.assert_called_once()

    @patch('model.ExpenseApp.Redis.get', return_value = None)
    def test_get_expense_by_id_error(self, mock_redis_get):
        app = ExpenseApp()
        mock_redis_get.return_value = None
        self.assertEqual(app.get_expense_by_id(2), ('Not Found', 404))
        mock_redis_get.assert_called_once()           
    
    @patch('model.ExpenseApp.Redis.exists', return_value = True)
    @patch('model.ExpenseApp.Redis.set')
    def test_update_expense(self, mock_redis_exists, mock_redis_set):
        app = ExpenseApp()         
        self.assertEqual(app.update_expense(1, TestRESTApp._testExpenseUpdate), TestRESTApp._testExpenseUpdate)
        mock_redis_exists.assert_called_once()
        mock_redis_set.assert_called_once()
    
    @patch('model.ExpenseApp.Redis.exists', return_value = True)
    @patch('model.ExpenseApp.Redis.get')
    @patch('model.ExpenseApp.Redis.delete')
    @patch('model.ExpenseApp.Redis.srem')
    def test_delete_expense(self, mock_redis_exists, mock_redis_get, mock_redis_delete, mock_redis_srem):
        app = ExpenseApp()
        mock_redis_get.return_value = json.dumps(TestRESTApp._testExpenseNew)  
        self.assertEqual(app.delete_expense(1), ('Deleted', 200))
        mock_redis_exists.assert_called_once()
        mock_redis_get.assert_called_once()
        mock_redis_delete.assert_called_once()
        mock_redis_srem.assert_called_once()       
    
    @patch('model.ExpenseApp.Redis')
    def test_find_expenses_by_tags(self, mock_redis):
        app = ExpenseApp()
        app.add_expense(TestRESTApp._testExpense)
        app.add_expense(TestRESTApp._testExpenseUpdate)
        expenses = app.find_expenses_by_tags(["daily"])
        self.assertEqual(expenses, [TestRESTApp._testExpenseUpdate])

    @patch('model.ExpenseApp.Redis')
    def test_get_all_expenses(self, mock_redis):
        app = ExpenseApp()
        app.add_expense(TestRESTApp._testExpense)
        app.add_expense(TestRESTApp._testExpenseUpdate)
        expenses = app.find_expenses_by_tags()
        self.assertEqual(expenses, [TestRESTApp._testExpense, TestRESTApp._testExpenseUpdate])

    @patch('model.ExpenseApp.Redis')
    def test_get_expenses_by_date(self, mock_redis):
        app = ExpenseApp()
        app.add_expense(TestRESTApp._testExpense)
        app.add_expense(TestExpenseDate2)
        expenses = app.find_expenses_by_date("2019-10-01")
        self.assertEqual(expenses, [TestRESTApp._testExpense])
    
    @patch('model.ExpenseApp.Redis')    
    def test_get_monthly_expenses(self, mock_redis):
        app = ExpenseApp()
        app.add_expense(TestRESTApp._testExpense)
        app.add_expense(TestExpenseDate2)
        expenseSummary = app.get_monthly_expenses(10)
        expectedSummary = {"month": 10, "sum": 3.7, "expenses": [TestRESTApp._testExpense, TestExpenseDate2]} 
        self.assertEqual(expenseSummary, expectedSummary)

if __name__ == '__main__':
    unittest.main(verbosity=2)