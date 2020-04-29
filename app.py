from flask import Flask, render_template, redirect, request, url_for
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'cookbook-app-db'
# DO NOT UPLOAD WITH URI
app.config['MONGO_URI'] = (
    "")

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
            exis_recipes = mongo.db.recipes
            exis_recipes.insert_one(request.form.to_dict())
            return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=(
        os.environ.get('PORT')), debug=True)
