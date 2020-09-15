from flask_wtf import FlaskForm
from app.models import Students
from app import db
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length


class LoginForm(FlaskForm):
    student_id = StringField("Student ID", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me?")
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    student_name = StringField('Student Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm your password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_registration(self, student_id):
        student = Students.query.filter_by(student_id=student_id.data).first()
        # student = db.query(Students).filter_by(student_id=student_id.data).first()
        if student is not None:
            raise ValidationError("An account is already registered under this id.")

    def validate_email(self, email):
        student = Students.query.filter_by(email=email.data).first()
        # student = db.query(Students).filter_by(email=email.data).first()
        if student is not None:
            raise ValidationError("An account is already registered under this email.")


class PostForm(FlaskForm):
    post_title = StringField('Your Post Title', validators=[DataRequired()])
    post_body = StringField(description='Content of your post', validators=[DataRequired(), Length(max=140)])
    submit = SubmitField('Post')
