from flask import Blueprint, render_template
from flask_login import login_required, current_user

# create views blueprint, this allows us to define functions before an actual object exists
views = Blueprint('views', __name__)

# this is the route to the home page
# the home page is a placeholder, if you want to change how it looks go to home.html
@views.route('/')
@login_required
def home():
    # render the homepage
    return render_template("home.html", user=current_user)

