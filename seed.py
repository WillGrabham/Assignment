import os
import random
from datetime import datetime

from flask_bcrypt import generate_password_hash

from website import create_app, db
from website.models import (
    Course,
    Module,
    Tutor,
    Student,
    CourseModule,
    StudentTutor,
    ModuleEnrolment,
)

if os.path.exists("./instance/site.db"):
    os.remove("./instance/site.db")

app = create_app()

courses = [
    Course(course_name="Psychology"),
    Course(course_name="Law"),
    Course(course_name="Engineering and Technology"),
    Course(course_name="Computer Science"),
    Course(course_name="Business and Management Studies"),
    Course(course_name="Mathematics"),
    Course(course_name="Criminology"),
    Course(course_name="Economics"),
    Course(course_name="Sport and Exercise"),
    Course(course_name="Technical Project Management"),
]

modules = [
    Module(module_name="Fundamentals of Software Engineering"),
    Module(module_name="How we think"),
    Module(module_name="Benefits of exercise"),
    Module(module_name="Project Management"),
    Module(module_name="Network security"),
    Module(module_name="The role of technology in the workplace"),
    Module(module_name="Data security"),
    Module(module_name="Geometry"),
    Module(module_name="People management"),
    Module(module_name="Demand and supply"),
]

course_modules = {
    "Psychology": ["How we think", "Benefits of exercise"],
    "Law": ["How we think", "Data security"],
    "Engineering and Technology": [
        "Fundamentals of Software Engineering",
        "Project Management",
        "The role of technology in the workplace",
        "Geometry",
    ],
    "Computer Science": [
        "Fundamentals of Software Engineering",
        "Project Management",
        "Network security",
        "The role of technology in the workplace",
        "Data security",
    ],
    "Business and Management Studies": ["Project Management", "People management"],
    "Mathematics": [
        "Fundamentals of Software Engineering",
        "Geometry",
        "Data security",
    ],
    "Criminology": ["How we think"],
    "Economics": ["How we think", "Demand and supply"],
    "Sport and Exercise": ["Benefits of exercise"],
    "Technical Project Management": [
        "How we think",
        "Fundamentals of Software Engineering",
        "Project Management",
        "The role of technology in the workplace",
        "People management",
    ],
}

tutor_names = [
    "Sharia Cartwright",
    "Keefe Maryman",
    "Shelden Marchington",
    "Antonin Boundley",
    "Latisha Bern",
    "Teena Gomersal",
    "Corbett Biskupski",
    "Lucias Petz",
    "Wenona Skim",
]

student_names = [
    "Ari Quene",
    "Lorraine Canedo",
    "Kristofer Folli",
    "Fleurette Pitrelli",
    "Rhonda Presslie",
    "Ilse Mantz",
    "Nadia Worlidge",
    "Rhetta Pass",
    "Corine Drohane",
    "Wandie Hunte",
]

with app.app_context():
    db.create_all()

    db.session.add_all(courses)
    db.session.add_all(modules)

    for tutor_name in tutor_names:
        tutor = Tutor(
            tutor_name=tutor_name,
            tutor_email=tutor_name.split(" ")[0].lower() + "@email.com",
            tutor_password=generate_password_hash("password").decode("utf-8"),
            is_admin=False,
        )
        db.session.add(tutor)

    db.session.add(
        Tutor(
            tutor_name="Will",
            tutor_email="admin@admin.com",
            tutor_password=generate_password_hash("password").decode("utf-8"),
            is_admin=True,
        )
    )

    for student_name in student_names:
        student = Student(
            student_name=student_name,
            student_email=student_name.split(" ")[0].lower() + "@email.com",
            join_date=datetime.now().date(),
            course_id=random.randint(1, 10),
        )
        db.session.add(student)

    db.session.commit()

    for course in courses:
        course_id = (
            Course.query.filter_by(course_name=course.course_name).first().course_id
        )
        modules = course_modules.get(course.course_name)
        for index, module in enumerate(modules):
            db.session.add(
                CourseModule(
                    course_id=course_id,
                    module_id=Module.query.filter_by(module_name=module)
                    .first()
                    .module_id,
                    module_order=index + 1,
                )
            )
    db.session.commit()

    for student in Student.query.all():
        db.session.add(
            StudentTutor(
                student_id=student.id,
                tutor_id=random.randint(1, 9),
            )
        )
        db.session.add(StudentTutor(student_id=student.id, tutor_id=10))
        number_of_modules = random.randint(3, 8)
        for module_id in random.sample(range(1, 10), number_of_modules):
            db.session.add(
                ModuleEnrolment(
                    student_id=student.id,
                    module_id=module_id,
                    grade=random.randint(40, 100),
                    grade_date=datetime.now().date(),
                )
            )

    db.session.commit()
