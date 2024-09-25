from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user
from models import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Signup successful. Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('todo.index'))
        flash('Invalid username or password')
    return render_template('login.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
