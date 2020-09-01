from flask import render_template, redirect, url_for
from flask_login import current_user, login_user
from app.forms import LoginForm
from app import app


@app.route('/')
@app.route('/index')
def homepage():
    return render_template('home.html', title="Home Page")


@app.route('/signup', methods=['POST', 'GET'])
def signup_page():
    return render_template('signup.html', title="Sign Up Page")


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    return render_template('login.html', title="Log In Page")

