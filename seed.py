from datetime import datetime

from flask_bcrypt import generate_password_hash

from app import create_app, db
from app.models import Student, Course, Module, CourseModule, ModuleEnrolment, Tutor, StudentTutor

app = create_app()

with app.app_context():
    db.create_all()

    course = Course(course_name="Course name")
    db.session.add(course)
    db.session.commit()

    new_course = Course.query.filter_by(course_name="Course name").first()
    student = Student(
        student_name="Student name",
        student_email="student@email.com",
        student_password=generate_password_hash('password').decode('utf-8'),
        join_date=datetime.now().date(),
        course_id=new_course.course_id)
    db.session.add(student)
    db.session.commit()

    module = Module(module_name="Module name")
    db.session.add(module)
    db.session.commit()

    new_module = Module.query.filter_by(module_name="Module name").first()
    courseModule = CourseModule(
        course_id=new_course.course_id,
        module_id=new_module.module_id,
        module_order=1)
    db.session.add(courseModule)
    db.session.commit()

    new_student = Student.query.filter_by(student_name="Student name").first()
    moduleEnrolment = ModuleEnrolment(
        student_id=new_student.student_id,
        module_id=new_module.module_id,
        grade=70,
        grade_date=datetime.now().date()
    )
    db.session.add(moduleEnrolment)
    db.session.commit()

    tutor = Tutor(
        tutor_name="Tutor name",
        tutor_contact_email="some-email@domain.com",
        tutor_email="admin@admin.com",
        tutor_password=generate_password_hash('password').decode('utf-8'),
        is_admin=True,
    )
    db.session.add(tutor)
    db.session.commit()

    new_tutor = Tutor.query.filter_by(tutor_name="Tutor name").first()
    student_tutor = StudentTutor(
        student_id=new_student.student_id,
        tutor_id=new_tutor.tutor_id
    )
    db.session.add(student_tutor)
    db.session.commit()
