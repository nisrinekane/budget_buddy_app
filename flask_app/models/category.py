from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash

DATABASE = 'expenses'

class Category:
    def __init__( self , data ):
        self.id = data['id']
        self.category_title = data['category_title']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_categories( cls ):
        query = "SELECT * FROM categories"
        results = connectToMySQL(DATABASE).query_db(query)
        expenses = []
        for row in results:
            # print(row)
            category = Category(row)
            # print(category.id)
            # print(category.cateory_title)
            expenses.append(category)
        return expenses

    # !get total by category
    @classmethod
    def get_total_by_category(cls, data):
        query = "SELECT SUM(amount) AS total,category_title AS category FROM expenses JOIN categories ON expenses.category_id = categories.id  WHERE user_id = %(id)s GROUP BY expenses.category_id;"
        return connectToMySQL(DATABASE).query_db(query, data)
        print(result)
