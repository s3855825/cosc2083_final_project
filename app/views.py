from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.forms import LoginForm, RegisterForm
from app import app, db
from app.models import Students


@app.route('/')
@app.route('/index')
@login_required
def homepage():
    return render_template('home.html', title="Home Page")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    register_form = RegisterForm()

    if register_form.validate_on_submit():
        student = Students(student_id=register_form.student_id.data,
                           student_name=register_form.student_name.data,
                           email=register_form.email.data)
        student.set_password(register_form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Account Registered. Redirecting to login.')
        # return redirect(url_for('login'))
        return render_template('register_success.html', title='Account created')
    return render_template('signup.html', title="Sign Up Page", form=register_form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        student_id = Students.query.filter_by(student_id=login_form.student_id.data).first()
        # student_id = db.query(Students).filter_by(student_id=login_form.student_id.data).first()
        if student_id is None or not student_id.check_password(login_form.password_hash.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(student_id, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Log In Page", form=login_form)


@app.route('/logout', methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for('login'))


# profile page
@app.route('/profile/<studentid>', methods=[])
@login_required
def profile(studentid):
    student = Students.query.filter_by(student_id=studentid).first_or_404()
    return render_template('profile.html', student=student)
