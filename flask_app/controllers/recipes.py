from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import recipe

@app.route('/recipes/add')
def add_recipe():
    return render_template("create_recipe.html")

@app.route('/recipes/create', methods = ['POST'])
def create_recipe():
    if not "user_id" in session:
        return redirect('/logout')
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'under_30_minutes' : request.form['under_30_minutes'],
        'user_id' : session['user_id'],
    }
    recipe_id = recipe.Recipe.create_recipe(data)
    if recipe_id:
        return redirect(f'/recipes/{recipe_id}')
    return redirect('/recipes/add')

@app.route('/recipes/<id>')
def show_recipe(id):
    if not "user_id" in session:
        return redirect('/logout')
    the_recipe = recipe.Recipe.get_recipe_by_id(id)
    return render_template("show_recipe.html", first_name = session['first_name'], recipe = the_recipe)

@app.route('/recipes/edit/<id>')
def edit_recipe(id):
    if "user_id" != "recipe.user.id":
        return redirect('logout')
    if not "user_id" in session:
        return redirect('/logout')
    the_recipe = recipe.Recipe.get_recipe_by_id(id)
    return render_template("edit_recipe.html", recipe = the_recipe)

@app.route('/recipes/update/<id>', methods = ['POST'])
def update_recipe(id):
    if "user_id" != "recipe.user.id":
        return redirect('logout')
    if not "user_id" in session:
        return redirect('/logout')
    data = {
        'id' : id,
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'under_30_minutes' : request.form['under_30_minutes'],
    }
    if recipe.Recipe.edit_recipe(data):
        return redirect(f'/recipes/{id}')
    return redirect(f'/recipes/edit/{id}')

@app.route('/recipes/delete/<id>')
def delete_recipe(id):
    if "user_id" != "recipe.user.id":
        return redirect('logout')
    if not "user_id" in session:
        return redirect('/logout')
    data = { 'id' : id}
    recipe.Recipe.delete_recipe(data)
    return redirect('/dashboard')