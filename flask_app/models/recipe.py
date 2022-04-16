from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app


class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30_minutes = data['under_30_minutes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create_recipe(cls, data):
        if not cls.validate_recipe(data):
            return False
        query = """
        INSERT INTO recipes (name, description, instructions, under_30_minutes, user_id) 
        VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30_minutes)s, %(user_id)s)
        ;"""
        return connectToMySQL('recipes_schema').query_db(query,data)

    @classmethod
    def get_recipe_by_id(cls, id):
        data = {'id' : id}
        query = """
        SELECT * FROM recipes 
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL('recipes_schema').query_db(query, data)
        if results:
            results = cls(results[0])
        return results

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes

    @classmethod
    def delete_recipe(cls, data):
        query = """
        DELETE FROM recipes 
        WHERE id = %(id)s
        ;"""
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def edit_recipe(cls, data):
        if not cls.validate_recipe(data):
            return False
        query = """
        UPDATE recipes 
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30_minutes = %(under_30_minutes)s
        WHERE id = %(id)s
        ;"""
        connectToMySQL('recipes_schema').query_db(query, data)
        return True

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False
        return is_valid
