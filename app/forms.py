from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField


class LoginForm:
    student_id = StringField()
    password_hash = PasswordField()
    remember_me = BooleanField()
    submit = SubmitField()


class SignUpForm:
    pass
