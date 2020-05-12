from flask import Flask, render_template, redirect, request, url_for,  session, flash
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_uploads import configure_uploads, IMAGES, UploadSet
import json

# App config
app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
# DO NOT UPLOAD WITH URI
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
mongo = PyMongo(app)
# Config for flask uploads
photos = UploadSet('photos', (IMAGES))
app.config['UPLOADED_PHOTOS_DEST'] = os.environ.get('UPLOADED_PHOTOS_DEST')
configure_uploads(app, photos)

# Default home page with search fucntion
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET' or request.form.get('search') == '':
        recipes = list(mongo.db.recipe.find())
        return render_template('home.html', recipes=recipes)
    else:
        search = request.form.get('search')
        recipes = mongo.db.recipe.find({'$text': {'$search': search}})
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
        recipe_img = photos.save(request.files['photo'])
        req = request.form
        new_recipe = {'author': req.get('author'), 'recipe_name': req.get('recipe_name'), 'recipe_desc': req.get('recipe_desc'), 'recipe_method': req.get('recipe_method'),
                      'recipe_ingredients': req.get('recipe_ingredients'), 'recipe_img': recipe_img, 'time': req.get('time'), 'serves': req.get('serves'), 'is_veggie': req.get('is_veggie'), 'is_vegan': req.get('is_vegan'), 'likes': 0}
        mongo.db.recipe.insert_one(new_recipe)
        return redirect(url_for('home'))


@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    recipe = mongo.db.recipe.find_one({'_id': ObjectId(recipe_id)})
    recipe_img = f"/static/uploads/{recipe.get('recipe_img')}"
    return render_template('viewrecipe.html', recipe=recipe, recipe_img=recipe_img)

# Edit finctionality if recipe is your own
@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = mongo.db.recipe.find_one({'_id': ObjectId(recipe_id)})
    if request.method == 'GET':
        return render_template('editrecipe.html', recipe=recipe)
    else:
        req = request.form
        update = {'$set': {'author': req.get('author'), 'recipe_name': req.get('recipe_name'), 'recipe_desc': req.get('recipe_desc'), 'recipe_method': req.get('recipe_method'),
                           'recipe_ingredients': req.get('recipe_ingredients'), 'time': req.get('time'), 'serves': req.get('serves'), 'is_veggie': req.get('is_veggie'), 'is_vegan': req.get('is_vegan')}}
        mongo.db.recipe.update_one(
            {'_id': ObjectId(recipe_id)}, update)
        return redirect(url_for('view_recipe', recipe_id=recipe_id))

        # View recipe

# Delete recipe if your own
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    recipe = mongo.db.recipe.find_one({'_id': ObjectId(recipe_id)})
# Removes image from MongoDatabase
    os.remove(os.path.join(
        app.config['UPLOADED_PHOTOS_DEST'], recipe.get('recipe_img')))
    mongo.db.recipe.delete_one({'_id': ObjectId(recipe_id)})
    return redirect(url_for('home'))

# Like functionality
@app.route('/like/<recipe_id>')
def like(recipe_id):
    if session.get('USERNAME'):
        if mongo.db.users.find_one({'username': session.get('USERNAME'), 'likes': recipe_id}, {'_id': 1}) == None:
            mongo.db.recipe.update_one({'_id': ObjectId(recipe_id)}, {
                '$inc': {'likes': 1}})
            mongo.db.users.update_one({'username': session['USERNAME']}, {
                '$push': {'likes': recipe_id}})
            flash('like added!')
        else:
            mongo.db.recipe.update_one({'_id': ObjectId(recipe_id)}, {
                '$inc': {'likes': -1}})
            mongo.db.users.update_one({'username': session['USERNAME']}, {
                '$pull': {'likes': recipe_id}})
            flash('like removed!')
    else:
        flash('You must be logged in to do that!')
    return redirect(url_for('view_recipe', recipe_id=recipe_id))


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
        else:
            flash('Your passwords must match! Please try again.')
            return redirect(url_for('create_account'))
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
