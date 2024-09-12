from flask import session
from flask_login import UserMixin

from website import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    if session['account_type'] == 'Student':
        return Student.query.get(int(user_id))
    elif session['account_type'] == 'Tutor':
        return Tutor.query.get(int(user_id))
    else:
        return None


class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80), unique=False, nullable=False)


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(80), unique=True, nullable=False)
    student_password = db.Column(db.String(80), unique=False, nullable=False)
    student_name = db.Column(db.String(80), unique=False, nullable=False)
    join_date = db.Column(db.Date, unique=False, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), unique=False, nullable=False)


class Tutor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    tutor_name = db.Column(db.String(80), unique=False, nullable=False)
    tutor_email = db.Column(db.String(80), unique=True, nullable=False)
    tutor_password = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class StudentTutor(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), primary_key=True)


class ModuleEnrolment(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), primary_key=True)
    grade = db.Column(db.Integer, unique=False, nullable=True)
    grade_date = db.Column(db.Date, unique=False, nullable=True)


class Module(db.Model):
    module_id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(80), unique=False, nullable=False)


class CourseModule(db.Model):
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), primary_key=True)
    module_order = db.Column(db.Integer, unique=False, nullable=False)


class DisplayModule:
    def __init__(self, module_id, module_order, module_name):
        self.module_id = module_id
        self.module_order = module_order
        self.module_name = module_name
