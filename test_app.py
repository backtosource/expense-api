import unittest

from appFunctions import AppFunctions

class TestRESTApp(unittest.TestCase):    

    def setUp(self):
        self.objectUnderTest = AppFunctions()
        self.TestExpense = {"value" : 1.2, "desc" : "Bread", "date" : "2019-10-01"}
        self.TestExpenseNew = {"value" : 1.2, "desc" : "Bread", "date" : "2019-10-01", "id" : 1}
        self.TestExpenseUpdate = {"value" : 1.2, "desc" : "Toast", "date" : "2019-10-01", "id" : 1}

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
        self.assertEquals(self.objectUnderTest.delete_expense(1), None)
        with self.assertRaises(KeyError) as raises:
            self.objectUnderTest.get_expense_by_id(1)

    def test_find_expenses_by_tags(self):
        self.objectUnderTest.add_expense(self.TestExpense)
        expenses = self.objectUnderTest.find_expenses_by_tags([])
        self.assertEqual(expenses, [self.TestExpense])


if __name__ == '__main__':
    unittest.main(verbosity=2)