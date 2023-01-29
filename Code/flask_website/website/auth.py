from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import json

# create auth blueprint, this allows us to define functions before an actual object exists
auth = Blueprint('auth', __name__)

# this is the route to the login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if post request:
    if request.method == 'POST':
        # get data from the forms
        username = request.form.get('username')
        password = request.form.get('password')
        # find user in database
        user = db.session.query(User).filter_by(username=username).first()
        # if the user exists, check the password hash, if these match, log in the user
        # if not flash error and do not login the user
        if user: 
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in succesfully.', category='success')
                return redirect(url_for('views.home'))
            else: 
                flash('Incorrect Password, try again.', category='error')
        else:
            flash('username does not exist.', category='error')
    # if get request:
    return render_template("login.html", user=current_user)

# this is the route to the logout page, it doesn't actually have any visuals.
# it logs out the current user and returns them to the login page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# this is the route to the change password page
# here users can change their passwords
@auth.route('/acc-pass', methods=['GET', 'POST'])
@login_required
def change_passwd():
    # if post request:
    if request.method == 'POST':
        # get info from forms
        current_password = request.form.get('current_password')
        new_password1 = request.form.get('new_password1')
        new_password2 = request.form.get('new_password2')

        # if the current password hash doesn't match the one filled in, flash error
        if not check_password_hash(current_user.password, current_password):
            flash('current password is incorrect', category='error')
        # if the new passwords don't match, flash error
        elif new_password1 != new_password2:
            flash('Passwords don\'t match', category='error')
        # if the password is too short, flash error
        elif len(new_password1) < 7 or len(new_password1) > 40:
            flash('Password must be 7-40 characters', category='error')
        # if everything is correct, generate new password hash and commit the new password to the database
        else: 
            current_user.password = generate_password_hash(new_password1, method='sha256')
            db.session.commit()
            flash('Succesfully changed password', category='succes')
            return redirect(url_for('views.home'))
    # if get request, render the page
    return render_template("change_password.html", user=current_user)