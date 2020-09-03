from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.forms import LoginForm
from app import app
from app.models import *


@app.route('/')
@app.route('/index')
@login_required
def homepage():
    return render_template('home.html', title="Home Page")


@app.route('/signup', methods=['POST', 'GET'])
def signup_page():
    return render_template('signup.html', title="Sign Up Page")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        student_id = Students.query.filter_by(student_id=form.student_id.data).first()
        if student_id is None or not student_id.check_password(form.password_hash.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(student_id, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Log In Page", form=form)


@app.route('/logout', methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for('login'))
