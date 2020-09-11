from werkzeug.security import check_password_hash, generate_password_hash
# from flask_login import UserMixin

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.types import Enum
# from app.database import base
from app import login_manager, db
from app import app
import enum


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}


class RoleEnum(enum.Enum):
    member = 'member'
    leader = 'leader'


@login_manager.user_loader
def load_student(student_id):
    return Students.get(int(student_id))


# class Students(UserMixin, base):
class Students(db.Model):
    __tablename__ = "Students"
    student_id = Column(String(7), primary_key=True, nullable=False, unique=True)
    email = Column(String(20), nullable=False, unique=True)
    student_name = Column(String(20), nullable=False)
    password_hash = Column(String)
    credit_score = Column(Float)

    def __init__(self, student_id, student_name, email):
        self.student_id = student_id
        self.student_name = student_name
        self.email = email

    def __repr__(self):
        return '<Student {}, {}>'.format(self.student_id, self.student_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# class WaitLists(base):
class WaitLists(db.Model):
    __tablename__ = "WaitLists"
    waitlist_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    student_id = Column(String(7), ForeignKey('Students.student_id'), unique=True)

    def __repr__(self):
        return '<Wait list {}>'.format(self.waitlist_id)


# class Posts(base):
class Posts(db.Model):
    __tablename__ = "Posts"
    post_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    message = Column(String(140))
    waitlist_id = Column(Integer, ForeignKey('WaitLists.waitlist_id'), unique=True)
    poster_id = Column(String(7), ForeignKey('Students.student_id'), unique=True)

    def __repr__(self):
        return '<Post {}, by {}, {}>'.format(self.post_id, self.poster_id, self.message[:50])


# class Courses(base):
class Courses(db.Model):
    __tablename__ = "Courses"
    course_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    course_code = Column(String(8), unique=True, nullable=False)
    course_name = Column(String(20), unique=True)

    def __repr__(self):
        return '<Course {}, {}>'.format(self.course_code, self.course_name)


# class CoursesTaken(base):
class CoursesTaken(db.Model):
    __tablename__ = "CoursesTaken"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    student_id = Column(String(7), ForeignKey('Students.student_id'))
    course_id = Column(Integer, ForeignKey('Courses.course_id'))
    semester = Column(String(10))
    gpa = Column(Float)

    def __repr__(self):
        return '<Course {}, taken by {} in {}, gpa {}>'.format(self.course_id, self.student_id, self.semester, self.gpa)


# class Reviews(base):
class Reviews(db.Model):
    __tablename__ = "Reviews"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    student1_id = Column(String(7), ForeignKey('Students.student_id'), unique=True)
    student2_id = Column(String(7), ForeignKey('Students.student_id'), unique=True)
    score = Column(Float)

    def __repr__(self):
        return '<User {}>'.format(self.username)


# class StudentGroups(base):
class StudentGroups(db.Model):
    __tablename__ = "StudentGroups"
    group_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    group_name = Column(String(10), unique=True, nullable=False)

    def __repr__(self):
        return '<Group {}, name {}>'.format(self.group_id, self.group_name)


# class GroupMembers(base):
class GroupMembers(db.Model):
    __tablename__ = "GroupMembers"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey('StudentGroups.group_id'))
    student_id = Column(String(7), ForeignKey('Students.student_id'))
    member_role = Column(Enum(RoleEnum), nullable=False)

    def __repr__(self):
        return '<Group member id {}, in group {} as {}>'.format(self.student_id, self.group_id, self.member_role)


# class Messages(base):
class Messages(db.Model):
    __tablename__ = "Messages"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    message = Column(String(140), nullable=False)
    sender_id = Column(String(7), ForeignKey('Students.student_id'), nullable=False)
    recipient_id = Column(String(7), ForeignKey('Students.student_id'), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)
