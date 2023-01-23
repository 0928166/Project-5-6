from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user: 
            if check_password_hash(user.password, password):
                flash('Logged in succesfully.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else: 
                flash('Incorrect Password, try again.', category='error')
        else:
            flash('username does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# @auth.route('/admin-page', methods=['GET', 'POST'])
# @login_required
# def admin_page():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         first_name = request.form.get('firstName')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')

#         user = User.query.filter_by(username=username).first()

#         if user:
#             flash('Username already in use', category='error')
#         elif len(username) < 4: 
#             flash('username invalid', category='error')
#         elif len(first_name) < 2:
#             flash('first name is invalid', category='error')
#         elif password1 != password2:
#             flash('Passwords don\'t match', category='error')
#         elif len(password1) < 7:
#             flash('Password must be 7 characters', category='error')
#         else: 
#             new_user = User(username=username, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
#             db.session.add(new_user)
#             db.session.commit()
            
#             flash('Account created!', category='succes')
#             return redirect(url_for('auth.admin_page'))
#     users = User.query.all()
#     return render_template("admin_page.html", user=current_user, users=users)   


# @auth.route('/delete-user', methods=['POST'])
# @login_required
# def delete_user():
#     data = json.loads(request.data)
#     userId = data['userId']
#     user = User.query.get(userId)
#     if user:
#         if user.id == userId:
#             db.session.delete(user)
#             db.session.commit()
#             return jsonify({})

@auth.route('/acc-pass', methods=['GET', 'POST'])
@login_required
def change_passwd():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password1 = request.form.get('new_password1')
        new_password2 = request.form.get('new_password2')

        if not check_password_hash(current_user.password, current_password):
            flash('current password is incorrect', category='error')
        elif new_password1 != new_password2:
            flash('Passwords don\'t match', category='error')
        elif len(new_password1) < 7:
            flash('Password must be 7 characters', category='error')
        else: 
            current_user.password = generate_password_hash(new_password1, method='sha256')
            db.session.commit()
            
            flash('Succesfully changed password', category='succes')
            return redirect(url_for('views.home'))
    return render_template("change_password.html", user=current_user)