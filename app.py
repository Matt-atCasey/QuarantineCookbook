from flask import Flask, render_template, redirect, request, url_for,  session, flash
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.filesystem import secure_filename
from flask_uploads import configure_uploads, IMAGES, UploadSet

# App config
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'cookbook-app-db'
# DO NOT UPLOAD WITH URI
app.config['MONGO_URI'] = (
    "")
app.config['SECRET_KEY'] = ''
mongo = PyMongo(app)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'
configure_uploads(app, photos)

# Default home page
@app.route('/')
def home():
    recipes = mongo.db.recipe.find()
    return render_template('home.html', recipes=recipes)

# Allows logged in users to add recipes to the database
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'GET':
        if 'USERNAME' in session:
            return render_template('addrecipe.html')
        else:
            flash('You must be logged in to add a recipe! Please log in now.')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        if 'photo' not in request.files:
            recipe_img = 'default.jpeg'
        else:
            req = request.form
            recipe_img = photos.save(secure_filename(request.files['photo']))
        new_recipe = {'author': req.get('author'), 'recipe_name': req.get('recipe_name'), 'recipe_desc': req.get('recipe_desc'), 'recipe_method': req.get('recipe_method'),
                      'recipe_ingredients': req.get('recipe_ingredients'), 'recipe_img': recipe_img, 'time': req.get('time'), 'serves': req.get('serves'), 'is_veggie': req.get('is_veggie'), 'is_vegan': req.get('is_vegan')}
        mongo.db.recipe.insert_one(new_recipe)
        return redirect(url_for('home'))

# Log in functionality
@app.route('/login', methods=['GET', 'POST'])
def login():
    # if the login form is recived:
    if request.method == 'POST':
        req = request.form
        username = req.get('username')
        password = req.get('password')
        # Try to grab from the database
        try:
            db_user = mongo.db.users.find_one({"username": username})
            db_pass = db_user.get('password')
        except:
            flash('Error accesing Database! Please try again.')
            return redirect(url_for('login'))
            # Compares the hashes of the form password and the password stored in the database for that user
        if check_password_hash(db_pass, password) == True:
            session['USERNAME'] = username
            flash(f'You have been logged in successfully, {username}')
            return redirect(url_for('home'))
        else:
            flash('Invalid user/pass. Please try again!')
            return render_template('login.html')
            # Else if loading page:
    elif request.method == 'GET':
        if session.get('USERNAME'):
            flash('You are already logged in!')
            return redirect(url_for('home'))
        else:
            return render_template('login.html')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        req = request.form
        username = req.get('username')
        password = req.get('password')
        confirm_password = req.get('confirm_password')
        users = mongo.db.users
        if password == confirm_password:
            try:
                if users.find_one({'username': username}) == None:
                    pass_hash = generate_password_hash(password)
                    new_user = {'username': username,
                                'password': pass_hash}
                    users.insert_one(new_user)
                else:
                    flash('This username is already taken! Please try again.')
                    return redirect(url_for('create_account'))
            except:
                flash('Database connection failed! Please try again.')
                return redirect(url_for('create_account'))
            session['USERNAME'] = username
            flash(
                f'Your account: ({username}) was created and you have been logged in successfully!')
            return redirect(url_for('home'))
    elif request.method == 'GET' and session.get('USERNAME'):
        username = session.get('USERNAME')
        flash('You are already logged in, {username}.')
        return redirect(url_for('home'))
    else:
        return render_template('createaccount.html')

# used for logout button to remove session
@app.route('/logout')
def logout():
    session.pop('USERNAME', None)
    flash('You have been logged out!')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=(
        os.environ.get('PORT')), debug=True)
