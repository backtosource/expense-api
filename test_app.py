import unittest

from appFunctions import expenses

class TestRESTApp(unittest.TestCase):    

    def setUp(self):
        self.objectUnderTest = expenses.Expenses()
        self.TestExpense = {"value" : 1.2, "desc" : "Bread", "date" : "2019-10-01", "tags" : ["food"]}
        self.TestExpenseNew = {"value" : 1.2, "desc" : "Bread", "date" : "2019-10-01", "id" : 1, "tags" : ["food"]}
        self.TestExpenseUpdate = {"value" : 1.2, "desc" : "Toast", "date" : "2019-10-01", "id" : 1, "tags" : ["food", "daily"]}
        self.TestExpenseDate2 = {"value" : 2.5, "desc" : "Apples", "date" : "2019-10-10", "tags" : ["food"]}
    def test_add_expense(self):       
        self.assertEqual(self.objectUnderTest.add_expense(self.TestExpense), self.TestExpenseNew)

    def test_get_expense_by_id(self):
        self.objectUnderTest.add_expense(self.TestExpense)
        self.assertEqual(self.objectUnderTest.get_expense_by_id(1), self.TestExpenseNew)

    def test_get_expense_by_id_error(self):
        with self.assertRaises(KeyError) as raises:
            self.objectUnderTest.get_expense_by_id(3)

    def test_update_expense(self):
        self.assertEqual(self.objectUnderTest.update_expense(self.TestExpenseUpdate), self.TestExpenseUpdate)
    
    def test_delete_expense(self):
        self.objectUnderTest.add_expense(self.TestExpense)
        self.assertEqual(self.objectUnderTest.delete_expense(1), None)
        with self.assertRaises(KeyError) as raises:
            self.objectUnderTest.get_expense_by_id(1)

    def test_find_expenses_by_tags(self):
        self.objectUnderTest.add_expense(self.TestExpense)
        self.objectUnderTest.add_expense(self.TestExpenseUpdate)
        expenses = self.objectUnderTest.find_expenses_by_tags(["daily"])
        self.assertEqual(expenses, [self.TestExpenseUpdate])

    def test_get_all_expenses(self):
        self.objectUnderTest.add_expense(self.TestExpense)
        self.objectUnderTest.add_expense(self.TestExpenseUpdate)
        expenses = self.objectUnderTest.find_expenses_by_tags()
        self.assertEqual(expenses, [self.TestExpense, self.TestExpenseUpdate])
    
    def test_get_expenses_by_date(self):
        self.objectUnderTest.add_expense(self.TestExpense)
        self.objectUnderTest.add_expense(self.TestExpenseDate2)
        expenses = self.objectUnderTest.find_expenses_by_date("2019-10-01")
        self.assertEqual(expenses, [self.TestExpense])
    
    def test_get_monthly_expenses(self):
        self.objectUnderTest.add_expense(self.TestExpense)
        self.objectUnderTest.add_expense(self.TestExpenseDate2)
        expenseSummary = self.objectUnderTest.get_monthly_expenses(10)
        expectedSummary = {"month": 10, "sum": 3.7, "expenses": [self.TestExpense, self.TestExpenseDate2]} 
        self.assertEqual(expenseSummary, expectedSummary)

if __name__ == '__main__':
    unittest.main(verbosity=2)