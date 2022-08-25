from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# PHONE_REGEX = re.compile(r'^\([0-9]{3}\)[0-9]{3}-[0-9]{4}$')
DATABASE = 'expenses'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.income = data['income']
        self.savings = data['savings']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.expenses = []

    # ! READ ALL THE USERS
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        # Iterate over the db results and create instances of users with cls.
        for user in results:
            users.append(cls(user))
        return users

    # ! READ/RETRIEVE ONE USER
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        user = User(result[0])
        return user

    # ! GET ONE USER BY EMAIL
    @classmethod
    def get_one_with_email(cls, data) -> object or bool:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        else:
            user = User(result[0])
        return user

    # ! CREATE/SAVE A USER TO THE DB (RETURNS AN ID)
    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! save user income/savings to db //set up user for first time
    @classmethod
    def get_income_savings(cls, data):
        query = "UPDATE users SET income = %(income)s, savings= %(savings)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! UPDATE/EDIT  a user
    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! get user savings
    @classmethod
    def get_savings(cls, data):
        query = "SELECT savings FROM users WHERE id=%(id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    # ! update user savings
    @classmethod
    def update_savings(cls, data):
        query = "UPDATE users SET savings= %(savings)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! VALIDATE A USER

    @staticmethod
    def validate_user(user:dict) -> bool:
        is_valid = True
        if len(user['first_name']) < 3:
            is_valid = False
            flash("Name must be at least 3 chars", 'first_name')
        if len(user['last_name']) < 3:
            is_valid = False
            flash("Name must be at least 3 chars", 'last_name')
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'email')
            is_valid = False
        if 'password' in user: #if the form has a pw field or if password is asked
            if user['password'] != user['password_confirmation']:
                flash("passwords must match!", 'password')
                is_valid = False
            if len(user['password']) < 8:
                flash('password must be at least 8 characters', 'password')
                is_valid = False
        return is_valid






    # ! validate a user info (income and savings)
    @staticmethod
    def validate_info(user):
        is_valid = True
        if not 'income':
            flash('Must enter income', 'income')
            is_valid = False
        if not 'savings':
            flash('Must enter savings', 'savings')
            is_valid = False
        return is_valid
