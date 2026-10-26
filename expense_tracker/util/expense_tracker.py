from .database import init_db,drop_table,get_expenses,display_expense
from .database import add_expense,delete_expense,update_expense,load_expense,summary

class ExpenseTracker:

    def __init__(self,db=init_db()):
        self.db = db

    def drop_t(self):
        drop_table()

    def add_exp(self,amount,description):
        add_expense(amount,description)

    def display_exp(self):
        return display_expense()

    def get_exp(self):
        get_expenses()

    def delete_exp(self,expense_id):
        delete_expense(expense_id)

    def update_exp(self,expense_id,amount,description):
        update_expense(expense_id,amount,description)

    def load_exp(self,expense_id):
        load_expense(expense_id)

    def summ_m(self,summary_m=True):
        return summary(summary_m=summary_m)

    def summ_categ(self,summary_categ):
        return summary(summary_categ=summary_categ)

    def summ_day(self,summary_day=True):
        return summary(summary_day=summary_day)

if __name__ == "__main__":
    e_tracker = ExpenseTracker()
    #e_tracker.add_exp(50,"Shopping For Food")
    #e_tracker.display_exp()
    #e_tracker.delete_exp(13)
    #e_tracker.update_exp(expense_id=13,amount=20,description="electricity bill")
    #e_tracker.load_exp(13)
    e_tracker.summ_m()
    e_tracker.summ_categ('utilities')
    e_tracker.summ_day()

    