from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models.user import User
DATABASE = 'expenses'

class Expense:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.amount = data['amount']
        self.category = data['category_id']
        if 'category_title' in data:
            self.category_title = data['category_title']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # self.total = data['total']


    # ! get all expenses
    @classmethod
    def all_expenses(cls, data):
        # "SELECT * FROM expenses JOIN users ON expenses.user_id = users.id"
        # query = "SELECT * FROM expenses JOIN users ON expenses.user_id = users.id WHERE expenses.user_id= %(id)s"
        query = "SELECT * FROM expenses JOIN categories ON expenses.category_id = categories.id WHERE user_id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        expenses = []
        for row in results:
            expenses.append(Expense(row))
        return expenses

    # # ! get all expenses for json
    # @classmethod
    # def all_expenses_json(cls, data):
    #     # "SELECT * FROM expenses JOIN users ON expenses.user_id = users.id"
    #     # query = "SELECT * FROM expenses JOIN users ON expenses.user_id = users.id WHERE expenses.user_id= %(id)s"
    #     # query = "SELECT SUM(amount) FROM expenses JOIN categories ON expenses.category_id = categories.id GROUP BY expenses.category_id WHERE user_id = %(id)s"
    #     results = connectToMySQL(DATABASE).query_db(query, data)
    #     print(results)
    #     # expenses = []
    #     # for row in results:
    #     #     expenses.append(Expense(row))
    #     return results

    # ! read/retrieve one expense by id
    @classmethod
    def get_one_expense(cls, data):
        query = "SELECT * FROM expenses WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return Expense(results[0])

    #! create an expense:
    @classmethod
    def create_expense(cls, data):
        query = "INSERT INTO expenses (name, amount, category_id, user_id) VALUES (%(name)s, %(amount)s, %(category_id)s, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! Delete an expense:
    @classmethod
    def delete_expense(cls, data):
        query = "DELETE FROM expenses Where id=%(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # ! total month expense
    @classmethod
    def total_expense(cls, data):
        query = "SELECT SUM(amount) FROM expenses WHERE user_id=%(id)s"
        result =  connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        return result
    
    # ! update/edit expense
    @classmethod
    def edit_expense(cls, data):
        query = "UPDATE expenses SET name = %(name)s, amount = %(amount)s, category_id = %(category_id)s WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)


    # ! calculate spending limit
    # ! get current month
    @classmethod
    def get_monthly_income(cls, data):
        query = "SELECT income FROM users WHERE id=%(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        print('***********************************')
        print(result)
        print('***********************************')
        return result


    #! validate an expense:
    @staticmethod
    def validate_expense(expense):
        is_valid = True
        if len(expense["name"]) <= 3:
            flash("Expense name must be at least 3 characters.", "expense")
            is_valid = False
        if len(expense["description"]) <= 3:
            flash("Description must be at least 3 characters.", "expense")
            is_valid = False
        if len(expense["category"]) == 0:
            flash("Pick expense category")
            is_valid = False
        if len(expense["amount"]) <= 0:
            flash("Amount must be greater than 0.", "expense")
            is_valid = False
        return is_valid






