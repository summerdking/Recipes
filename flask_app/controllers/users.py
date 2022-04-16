from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models import user, recipe

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def landing_page():
    return render_template("index.html")

@app.route('/register', methods = ['POST'])
def register_user():
    if user.User.create_user(request.form):
        return redirect('/dashboard')
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login_user():
    if user.User.validate_login(request.form):
        return redirect('/dashboard')
    return redirect('/')

@app.route('/dashboard')
def show_users_dash():
    if session.get('user_id'):
        recipes = recipe.Recipe.get_all_recipes()
        return render_template("dashboard.html", first_name = session['first_name'], recipes = recipes)
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')