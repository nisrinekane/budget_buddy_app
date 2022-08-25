from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models.user import User
DATABASE = 'expenses'


class Fund:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.amount = data['amount']
        self.category = data['category_id']
        if 'category_title' in data:
            self.category_title = data['category_title']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # self.total = data['total']


    # ! read/retrieve one expense by id
    @classmethod
    def get_one_fund(cls, data):
        query = "SELECT * FROM funds WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return Fund(results[0])

    # ! Delete a fund:
    @classmethod
    def delete_fund(cls, data):
        query = "DELETE FROM funds Where id=%(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    
    # ! update/edit funds
    @classmethod
    def edit_fund(cls, data):
        query = "UPDATE funds SET name = %(name)s, description = %(description)s, amount = %(amount)s, category_id = %(category_id)s WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! get all funds
    @classmethod
    def all_funds(cls, data):
        # "SELECT * FROM expenses JOIN users ON expenses.user_id = users.id"
        # query = "SELECT * FROM expenses JOIN users ON expenses.user_id = users.id WHERE expenses.user_id= %(id)s"
        query = "SELECT * FROM funds JOIN categories ON funds.category_id = categories.id WHERE user_id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        funds = []
        for row in results:
            funds.append(Fund(row))
        return funds

    #! create a fund:
    @classmethod
    def create_fund(cls, data):
        query = "INSERT INTO funds (name, description, amount, category_id, user_id) VALUES (%(name)s, %(description)s, %(amount)s, %(category_id)s, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    