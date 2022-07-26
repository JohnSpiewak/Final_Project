from mysqlconnection import connectToMySQL
from flask import flash
import re
db = 'songs_schema'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user_dict in results:
            user = cls(user_dict)
            users.append(user)
        return users

    @classmethod
    def create_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL(db).query_db(query,data)
        return results

    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users Where id = %(user_id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        user = cls(results[0])
        return user

        
    @classmethod
    def delete(cls, user_id):
        query = f"DELETE FROM users WHERE id = {user_id}"
        results = connectToMySQL(db).query_db(query)
        return results

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)

        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_user(user_info):
        is_valid = True
        print(user_info)
        if not EMAIL_REGEX.match(user_info['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(user_info['first_name']) < 3:
            flash('First Name must be greater than 2 characters.')
            is_valid = False
        if len(user_info['last_name']) < 3:
            flash('Last Name must be greater than 2 characters.')
            is_valid = False
        if len(user_info['password']) < 8:
            flash('Password must be greater than 7 characters.')
            is_valid = False
        if user_info['confirm_pw'] != user_info['password']:
            flash("Your passwords do not match.")
            is_valid = False
        return is_valid
        
