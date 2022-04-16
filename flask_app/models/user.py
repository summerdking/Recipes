from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
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
        self.recipes = []

    @classmethod
    def create_user(cls, data):
        if not cls.validate_user_registration(data):
            return False
        data = cls.parse_registration(data)
        query = """
        INSERT INTO users (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL('recipes_schema').query_db(query,data)
        session['user_id'] = user_id
        session['first_name'] = data['first_name']
        return user_id

    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email}
        query = """
        SELECT * FROM users 
        WHERE email = %(email)s
        ;"""
        results = connectToMySQL('recipes_schema').query_db(query, data)
        if results:
            results = cls(results[0])
        return results

    @staticmethod
    def validate_user_registration(data):
        is_valid = True
        if User.get_user_by_email(data['email'].lower()):
            flash("Email already taken.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Email not valid.")
            is_valid = False
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Password does not match.")
            is_valid = False
        return is_valid

    @staticmethod
    def parse_registration(data):
        parsed_data = {
        'email' : data['email'].lower(),
        'password' : bcrypt.generate_password_hash(data['password']),
        'first_name' : data['first_name'],
        'last_name' : data['last_name'],
        }
        return parsed_data

    @staticmethod
    def validate_login(data):
        user = User.get_user_by_email(data['email'].lower())
        if user:
            if bcrypt.check_password_hash(user.password, data['password']):
                session['user_id'] = user.id
                session['first_name'] = user.first_name
                return True
        flash("Email and/or password is incorrect.")
        return False
