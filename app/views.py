from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.forms import LoginForm, RegisterForm, PostForm
from app import app, db
from app.models import Students, Posts, StudentGroups


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title="Home Page")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    register_form = RegisterForm()

    if register_form.validate_on_submit():
        # print('form validated')
        student = Students(student_id=register_form.student_id.data,
                           student_name=register_form.student_name.data,
                           email=register_form.email.data)
        student.set_password(register_form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Account Registered. Redirecting to index.')
        return redirect(url_for('index'))
    # print('form not validated')
    return render_template('signup.html', title="Sign Up Page", form=register_form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        # print('form validated')
        student_id = Students.query.filter_by(id=login_form.student_id.data).first()
        # student_id = db.query(Students).filter_by(student_id=login_form.student_id.data).first()
        if student_id is None or not student_id.check_password(login_form.password_hash.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(student_id, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            print('not next page')
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Log In Page", form=login_form)


@app.route('/logout', methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile/<studentid>', methods=['POST', 'GET'])
@login_required
def profile(studentid):
    student = Students.query.filter_by(id=studentid).first_or_404()
    # posts = [
    #     {'author': student, 'message': 'Test post #1'},
    #     {'author': student, 'message': 'Test post #2'}
    # ]
    posts = Posts.query.filter_by(poster_id=current_user.id).all()
    if not posts:
        posts = [{'poster_id': '', 'post_title': 'No post made yet :<', 'message': ''}]
    print(posts)
    return render_template('profile.html', student=student, posts=posts)
    # return render_template('profile.html', student=student)


@app.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    post_form = PostForm()

    if post_form.validate_on_submit():
        post = Posts(post_title=post_form.post_title.data,
                     message=post_form.post_body.data,
                     poster_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('post.html', title='Create post', form=post_form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    posts = Posts.query.all()
    if not posts:
        posts = [{'poster_id': 'Admin', 'message': 'No post made yet :<'}]
    return render_template('dashboard.html', title='Dashboard', posts=posts)


@app.route('/group', methods=['GET', 'POST'])
@login_required
def group():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    group = StudentGroups.query.filter_by()
    return render_template('group.html', title='Group Page')
