from flask import Flask, render_template, redirect, request, url_for, session, flash
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'cookbook-app-db'
# DO NOT UPLOAD WITH URI
app.config['MONGO_URI'] = (
    "")
app.config['SECRET_KEY'] = ''
mongo = PyMongo(app)

# Default home page
@app.route('/')
def home():
    recipes = mongo.db.recipe.find()
    return render_template('home.html', recipes=recipes)


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'GET':
        return render_template('addrecipe.html')
    else:
        if request.method == 'POST':
            exis_recipes = mongo.db.recipe
            exis_recipes.insert_one(request.form.to_dict())
            return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        req = request.form
        username = req.get('username')
        password = req.get('password')
        print(username+password)
        try:
            db_user = mongo.db.users.find_one({"username": username})
            db_pass = db_user.get('password')
        except:
            flash('Error accesing Database! Please try again.')
            return redirect(url_for('login'))
        print(db_user)
        print(db_user.get('password'))
        if check_password_hash(db_pass, password) == True:
            session['USERNAME'] = username
            print(session['USERNAME'])
            flash(f'You have been logged in successfully, {username}')
            return redirect(url_for('home'))
        else:
            print(check_password_hash(db_user.get('password'), password))
            print(session.get('USERNAME'))
            flash('Invalid user/pass. Please try again!')
            return render_template('login.html')
    elif request.method == 'GET':
        if session.get('USERNAME'):
            flash('You are already logged in!')
            return redirect(url_for('home'))
        else:
            return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('USERNAME', None)
    flash('You have been logged out!')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=(
        os.environ.get('PORT')), debug=True)
