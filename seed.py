import os
from datetime import datetime

from flask_bcrypt import generate_password_hash

from website import create_app, db
from website.models import (
    Student,
    Course,
    Module,
    CourseModule,
    ModuleEnrolment,
    Tutor,
    StudentTutor,
)

course_name = "Computer Science"
module_name = "Software Engineering"
module_name_two = "Network Engineering"
student_name = "Ercan"
student_name_two = "Jonny"
tutor_name = "Pete"

if os.path.exists("./instance/site.db"):
    os.remove("./instance/site.db")

app = create_app()

with app.app_context():
    db.create_all()

    course = Course(course_name=course_name)
    db.session.add(course)
    db.session.commit()

    new_course = Course.query.filter_by(course_name=course_name).first()
    student = Student(
        student_name=student_name,
        student_email=student_name + "@email.com",
        join_date=datetime.now().date(),
        course_id=new_course.course_id,
    )
    student_two = Student(
        student_name=student_name_two,
        student_email=student_name_two + "@email.com",
        join_date=datetime.now().date(),
        course_id=new_course.course_id,
    )
    db.session.add(student)
    db.session.add(student_two)
    db.session.commit()

    module = Module(module_name=module_name)
    db.session.add(module)
    module_two = Module(module_name=module_name_two)
    db.session.add(module_two)
    db.session.commit()

    new_module = Module.query.filter_by(module_name=module_name).first()
    new_module_two = Module.query.filter_by(module_name=module_name_two).first()
    courseModule = CourseModule(
        course_id=new_course.course_id, module_id=new_module.module_id, module_order=1
    )
    db.session.add(courseModule)
    courseModuleTwo = CourseModule(
        course_id=new_course.course_id,
        module_id=new_module_two.module_id,
        module_order=2,
    )
    db.session.add(courseModuleTwo)
    db.session.commit()

    new_student = Student.query.filter_by(student_name=student_name).first()
    new_student_two = Student.query.filter_by(student_name=student_name_two).first()
    moduleEnrolment = ModuleEnrolment(
        student_id=new_student.id,
        module_id=new_module.module_id,
        grade=99,
        grade_date=datetime.now().date(),
    )
    moduleEnrolmentTwo = ModuleEnrolment(
        student_id=new_student.id,
        module_id=new_module_two.module_id,
        grade=70,
        grade_date=datetime.now().date(),
    )
    moduleEnrolmentThree = ModuleEnrolment(
        student_id=new_student_two.id,
        module_id=new_module.module_id,
        grade=40,
        grade_date=datetime.now().date(),
    )
    db.session.add(moduleEnrolment)
    db.session.add(moduleEnrolmentTwo)
    db.session.add(moduleEnrolmentThree)
    db.session.commit()

    tutor = Tutor(
        tutor_name=tutor_name,
        tutor_email="admin@admin.com",
        tutor_password=generate_password_hash("password").decode("utf-8"),
        is_admin=True,
    )
    db.session.add(tutor)
    db.session.commit()

    new_tutor = Tutor.query.filter_by(tutor_name=tutor_name).first()
    student_tutor = StudentTutor(student_id=new_student.id, tutor_id=new_tutor.id)
    student_tutor_two = StudentTutor(
        student_id=new_student_two.id, tutor_id=new_tutor.id
    )
    db.session.add(student_tutor)
    db.session.add(student_tutor_two)
    db.session.commit()
