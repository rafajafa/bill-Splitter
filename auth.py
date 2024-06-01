# from flask import Flask, request, Blueprint, redirect, url_for, flash, render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import current_user, login_user, logout_user, login_required

# from app import db
# from forms import RegistrationForm, LoginForm
# from app_models import AppUser

# auth = Blueprint('auth', __name__)

# # Register route
# @auth.route('/register', methods=['Get','POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         # from app_models import AppUser
        
#         user = AppUser(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('auth.login'))
#     return render_template('register.html', title='Register', form=form)

# # Login route
# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         # from app_models import AppUser
        
#         user = AppUser.query.filter_by(email=form.email.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('auth.login'))
#         login_user(user)
#         return redirect(url_for('index'))
#     return render_template('login.html', title='Sign In', form=form)

# # Logout route
# @auth.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

