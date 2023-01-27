from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from . import db 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required, logout_user, current_user
import json
# create admin blueprint, this allows us to define functions before an actual object exists
admin = Blueprint('admin', __name__)

# this will be the route to get to the adminpage, this is only reachable if you are logged in and an admin user.
@admin.route('/admin-page', methods=['GET', 'POST'])
@login_required
def admin_page():
    # check if the user is an admin user, if not return the user to the homepage
    if not current_user.is_admin:
        return redirect(url_for('views.home'))
    # if a post request has been made (a request to create a new user):
    if request.method == 'POST':
        # get the info from the forms
        username = request.form.get('username')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # search the database for a user with the same username
        user = User.query.filter_by(username=username).first()
        # if one is found, flash error msg
        if user:
            flash('Username already in use', category='error')
        # if username is too short, flash error
        elif len(username) < 4: 
            flash('username invalid', category='error')
        # if the first name is too short, flash error
        elif len(first_name) < 2:
            flash('first name is invalid', category='error')
        # if passwords aren't the same, flash error
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        # if the password is not a min of 7 characters, flash error
        elif len(password1) < 7:
            flash('Password must be 7 characters', category='error')
        # if everything is correct, create user and hash the password and commit the user to the database
        else: 
            new_user = User(username=username, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='succes')
            return redirect(url_for('admin.admin_page'))

    # if it is just a get request. get all the users, render the adminpage
    users = User.query.all()
    return render_template("admin_page.html", user=current_user, users=users) 

  
# this route is only used when the admin decided to remove a user, it will take the json made by the js script deleteuser
@admin.route('/delete-user', methods=['POST'])
@login_required
def delete_user():
    # read the json made by the script, take the user id and search it in the database
    data = json.loads(request.data)
    userId = data['userId']
    user = User.query.get(userId)
    # if the user is found, get the id and delte the user and commit the database
    if user:
        if user.id == userId:
            db.session.delete(user)
            db.session.commit()
            return jsonify({})