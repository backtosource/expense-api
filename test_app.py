from model.ExpenseApp import ExpenseApp
from unittest import TestCase
from unittest.mock import patch
import unittest
import json

class TestRESTApp(TestCase):   

    _testExpense = {"value" : 1.2, "desc" : "Bread", "date" : "2019-10-01", "tags" : ["food"]}
    _testExpenseNew = {"value" : 1.2, "desc" : "Bread", "date" : "2019-10-01", "id" : "id_1", "tags" : ["food"]}
    _testExpenseUpdate = {"value" : 1.2, "desc" : "Toast", "date" : "2019-10-01", "id" : "id_2", "tags" : ["food", "daily"]}
    _testExpenseDate2 = {"value" : 2.5, "desc" : "Apples", "date" : "2019-10-10", "tags" : ["food"]}
 
    @patch('model.ExpenseApp.Redis')
    def test_add_expense(self, mock_redis):
        app = ExpenseApp()
        mock_redis.return_value.incr.return_value = 1                      
        self.assertEqual(app.add_expense(TestRESTApp._testExpense), TestRESTApp._testExpenseNew)
        mock_redis.return_value.incr.assert_called_once()
        mock_redis.return_value.set.assert_called_once()
        mock_redis.return_value.sadd.assert_called_once()

    @patch('model.ExpenseApp.Redis')
    def test_get_expense_by_id(self, mock_redis):
        app = ExpenseApp()
        mock_redis.return_value.get.return_value = json.dumps(TestRESTApp._testExpenseNew)
        self.assertEqual(app.get_expense_by_id('id_1'), TestRESTApp._testExpenseNew)
        mock_redis.return_value.get.assert_called_once()

    @patch('model.ExpenseApp.Redis')
    def test_get_expense_by_id_error(self, mock_redis):
        app = ExpenseApp()
        mock_redis.return_value.get.return_value = None
        self.assertEqual(app.get_expense_by_id('id_2'), ('Not Found', 404))
        mock_redis.return_value.get.assert_called_once()           
    
    @patch('model.ExpenseApp.Redis')    
    def test_update_expense(self, mock_redis):
        app = ExpenseApp()
        mock_redis.return_value.exists.return_value = True         
        self.assertEqual(app.update_expense('id_1', TestRESTApp._testExpenseUpdate), TestRESTApp._testExpenseUpdate)
        mock_redis.return_value.exists.assert_called_once()
        mock_redis.return_value.set.assert_called_once()
    
    @patch('model.ExpenseApp.Redis')    
    def test_delete_expense(self, mock_redis):
        app = ExpenseApp()
        mock_redis.return_value.exists.return_value = True
        mock_redis.return_value.get.return_value = json.dumps(TestRESTApp._testExpenseNew)  
        self.assertEqual(app.delete_expense('id_1'), ('Deleted', 200))
        mock_redis.return_value.exists.assert_called_once()
        mock_redis.return_value.get.assert_called_once()
        mock_redis.return_value.delete.assert_called_once()
        mock_redis.return_value.srem.assert_called_once()       
    
    @patch('model.ExpenseApp.Redis')
    def test_find_expenses_by_tags(self, mock_redis):
        app = ExpenseApp()
        mock_redis.return_value.scan_iter.return_value = ['id_1', 'id_2']        
        mock_redis.return_value.get.side_effect = [json.dumps(TestRESTApp._testExpenseNew), json.dumps(TestRESTApp._testExpenseUpdate)]
        expenses = app.find_expenses_by_tags(['daily'])
        self.assertEqual(expenses, [TestRESTApp._testExpenseUpdate])

    @patch('model.ExpenseApp.Redis')    
    def test_get_all_expenses(self, mock_redis):
        app = ExpenseApp()
        mock_redis.return_value.scan_iter.return_value = ['id_1', 'id_2']        
        mock_redis.return_value.get.side_effect = [json.dumps(TestRESTApp._testExpenseNew), json.dumps(TestRESTApp._testExpenseUpdate)]
        expenses = app.find_expenses_by_tags()
        self.assertEqual(expenses, [TestRESTApp._testExpenseNew, TestRESTApp._testExpenseUpdate])

    @patch('model.ExpenseApp.Redis')
    def test_get_expenses_by_date(self, mock_redis):
        app = ExpenseApp()
        mock_redis.return_value.smembers.return_value = ['id_1', 'id_2']
        mock_redis.return_value.get.side_effect = [json.dumps(TestRESTApp._testExpenseNew), json.dumps(TestRESTApp._testExpenseUpdate)]  
        expenses = app.find_expenses_by_date("2019-10-01")
        self.assertEqual(expenses, [TestRESTApp._testExpenseNew, TestRESTApp._testExpenseUpdate])
    
    @patch('model.ExpenseApp.Redis')    
    def test_get_monthly_expenses(self, mock_redis):
        app = ExpenseApp()
        mock_redis.return_value.scan_iter.return_value = ['2019-10-01', '2019-10-10']
        mock_redis.return_value.get.side_effect = ['id_1', 'id_2', json.dumps(TestRESTApp._testExpenseNew), json.dumps(TestRESTApp._testExpenseUpdate)]
        expenseSummary = app.get_monthly_expenses('2019-10')
        expectedSummary = {"year_month": "2019-10", "sum": 2.4, "expenses": [TestRESTApp._testExpenseNew, TestRESTApp._testExpenseUpdate]} 
        self.assertEqual(expenseSummary, expectedSummary)

if __name__ == '__main__':
    unittest.main(verbosity=2)