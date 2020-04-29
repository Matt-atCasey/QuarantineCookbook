from flask import Flask, render_template, redirect, request, url_for
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'cookbook-app-db'
# DO NOT UPLOAD WITH URI
app.config['MONGO_URI'] = (
    "<mongoURI>")

mongo = PyMongo(app)


@app.route('/')
def home():
    recipes = mongo.db.recipe.find()
    return render_template('home.html', recipes=recipes)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=(
        os.environ.get('PORT')), debug=True)
