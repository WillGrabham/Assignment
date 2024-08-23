from app import db


class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80), unique=False, nullable=False)


class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(80), unique=True, nullable=False)
    student_password = db.Column(db.String(80), unique=False, nullable=False)
    student_name = db.Column(db.String(80), unique=False, nullable=False)
    join_date = db.Column(db.Date, unique=False, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), unique=False, nullable=False)


class Tutor(db.Model):
    tutor_id = db.Column(db.Integer, primary_key=True)
    tutor_name = db.Column(db.String(80), unique=False, nullable=False)
    tutor_contact_email = db.Column(db.String(80), unique=False, nullable=False)
    tutor_email = db.Column(db.String(80), unique=True, nullable=False)
    tutor_password = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class StudentTutor(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.tutor_id'), primary_key=True)


class ModuleEnrolment(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), primary_key=True)
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
