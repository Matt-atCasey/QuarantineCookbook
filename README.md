# Quarantine Cookbook

This website is a way for users to share and edit their recipes with the community.
Users can create an account and upload their recipe with a picture and 'like' other users recipes too.
It is catered towards the beginners and intermediate cooks, with a simple way to create a recipe without complex builders 
and countless chunks of nutritional information.

## UX

This website is designed to be as simple and to point as it can be. Loading the site brings you toa list of recipes that users
have created as well as a searchbar to easily search through the title and description of recipes. Along with brief
descriptions, how long they take to make and how many peoeple the recipe serves. Clicking the recipe brings you to further information
with ingredients, method and some extra information such as if the recipe is vegan, the author and how manyt likes the recipe has recived.

In order to create a recipe, we ask users to log in or create an account (passwords are only stored in a hash to be secure) so that we can
store their user information such as likes and author name. You can then create your recip, specify the information along with it and upload
it to the site for others to see. If you need to change anything later, you can edit or delete (as long as you're the author) the recipe.

### User Stories
  * As a Teenager confined to isolating at home, I want to try baking. I can go onto QuarantineCookbook and without needing to even create
an account, use the seachbar on the home page to seach for recipes that include the word cookies so that I can compare and then use as
a guide to learn. I then leave it a like so others can see I found it useful
  * As a parent, I am an intermidiate cook been experimenting with different recipe ideas and would like to share them. I click on create
recipe, see I have to make an account and then upload it stright to the front page.

## Features

  * Allows users to view recipes by either searching for key words or clicking on recipe cards to see their full information.
  * Create an account by clicking on the user icon in the nav bar and then the 'Create Account' text to fill out your user form.
  * Leave a like on recipes by logging in, selecting your favourite recipe and clicking the like button to add or remove likes.
  * Create a recipe by logging in and then clicking the add recipe icon in the nav bar to fill out the form required to post.
  * Edit or delete your recipe by clicking on a recipe, if it is yours, an edit and delete button will show at the bottom of the card.
Click edit to edit the form your submitted, or delete to remove your recipe and picture from the database.

### Future Ideas
  * Implement 'Sort-by' for likes and possibly other filters.
  * Pagination for when there is many recipes on page.

## Technologies Used
This project uses:
  * HTML 5
  * CSS
  * [Materialize 1.0](https://materializecss.com/) - Used for simple styling and layout.
  * [MongoDB](https://www.mongodb.com/) - Used for the database for the users and recipes.
  * Flask - Web Framework
  * Jinja - Web Templating language for Python
  * [Flask-Uploads](https://github.com/maxcountryman/flask-uploads) - Used for image uploading and saving in recipe form.
  * Werkzeug Library - For password hashing and verifying.
  * [Pymongo](https://pymongo.readthedocs.io/) - Mongo Api for python for easier implimentation of mongodb.
  * [Heroku](https://heroku.com/) - Used to host the site.


## Deployment

This site is deployed [HERE](http://quarantinecookbook.herokuapp.com/add_recipe) on Heroku.  
Heroku config variables are used in order to conceal the Mongo URI and the session secret Key. Along with all other app
config variables.

## Testing
  * Went through the site with my tutor checking major flaws there could be with the site. For example, checking authentication
  was working properly and did not allow non users into parts of the site that they shouldnt be.
  * went through the user stories to make sure that the site worked as intended.
  * Forwarded site to users without giving them context of the site to see if the ux and ui was easily understood. 
  Which it seemed to be.

## Credits
All work was done by me.
