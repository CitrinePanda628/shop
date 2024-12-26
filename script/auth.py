import re
from flask import Blueprint, flash, redirect, render_template, request, url_for
from script.database import User, db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('exampleInputEmail1')
        password = request.form.get('exampleInputPassword1')

        if email and password:
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                flash('Access granted.', category='success')
                return render_template('home/web.html')
            flash('Invalid credentials.', category='danger')
        else:
            flash('Please fill out all fields.', category='danger')

        return redirect(url_for('auth.login'))

    return render_template('login-sign/login.html')

@auth.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        email = request.form.get('exampleInputEmail1')
        password = request.form.get('exampleInputPassword1')

        if email and password:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already used.', category='danger')
            elif not is_valid_email(email):
                flash('Invalid email format.', category='danger')
            elif len(password) < 4:
                flash('Password too short.', category='danger')
            else:
                hashed_password = generate_password_hash(password)
                new_user = User(email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully.', category='success')
                return redirect(url_for('auth.login'))
        else:
            flash('Please fill out all fields.', category='danger')

        return redirect(url_for('auth.signin'))

    return render_template('login-sign/signin.html')

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
