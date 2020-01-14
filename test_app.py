import sys, unittest, app

class TestRESTApp(unittest.TestCase):   

    @classmethod
    def setUpClass(self):
        self.TestExpense = {"value" : 1.2, "desc" : "Bread", "date" : "2019-10-01", "tags" : ["food"]}
        self.TestExpenseNew = {"value" : 1.2, "desc" : "Bread", "date" : "2019-10-01", "id" : 1, "tags" : ["food"]}
        self.TestExpenseUpdate = {"value" : 1.2, "desc" : "Toast", "date" : "2019-10-01", "id" : 1, "tags" : ["food", "daily"]}
        self.TestExpenseDate2 = {"value" : 2.5, "desc" : "Apples", "date" : "2019-10-10", "tags" : ["food"]}

    def setUp(self):        
        app.resetApp()
 
    def test_add_expense(self):              
        self.assertEqual(app.add_expense(self.TestExpense), self.TestExpenseNew)

    def test_get_expense_by_id(self):
        app.add_expense(self.TestExpense)
        self.assertEqual(app.get_expense_by_id(1), self.TestExpenseNew)

    def test_get_expense_by_id_error(self):
        app.add_expense(self.TestExpense)
        self.assertEqual(app.get_expense_by_id(2), ('Not Found', 404))            

    def test_update_expense(self):
        app.add_expense(self.TestExpense)
        self.assertEqual(app.update_expense(1, self.TestExpenseUpdate), self.TestExpenseUpdate)
    
    def test_delete_expense(self):
        app.add_expense(self.TestExpense)
        self.assertEqual(app.delete_expense(1), ('Deleted', 200))        

    def test_find_expenses_by_tags(self):
        app.add_expense(self.TestExpense)
        app.add_expense(self.TestExpenseUpdate)
        expenses = app.find_expenses_by_tags(["daily"])
        self.assertEqual(expenses, [self.TestExpenseUpdate])

    def test_get_all_expenses(self):
        app.add_expense(self.TestExpense)
        app.add_expense(self.TestExpenseUpdate)
        expenses = app.find_expenses_by_tags()
        self.assertEqual(expenses, [self.TestExpense, self.TestExpenseUpdate])
    
    def test_get_expenses_by_date(self):
        app.add_expense(self.TestExpense)
        app.add_expense(self.TestExpenseDate2)
        expenses = app.find_expenses_by_date("2019-10-01")
        self.assertEqual(expenses, [self.TestExpense])
    
    def test_get_monthly_expenses(self):
        app.add_expense(self.TestExpense)
        app.add_expense(self.TestExpenseDate2)
        expenseSummary = app.get_monthly_expenses(10)
        expectedSummary = {"month": 10, "sum": 3.7, "expenses": [self.TestExpense, self.TestExpenseDate2]} 
        self.assertEqual(expenseSummary, expectedSummary)

if __name__ == '__main__':
    unittest.main(verbosity=2)