from datetime import datetime
from functools import wraps

from flask import redirect, render_template, url_for, Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from website import bcrypt, db
from website.api import (
    get_student_grades,
    get_student_name,
    get_students_for_tutor,
    get_all_modules,
    get_all_module_ids,
    get_student_enrolments,
    get_all_courses,
    get_modules_for_course,
)
from website.forms import (
    TutorLoginForm,
    TutorAddStudentGradeForm,
    TutorCreateStudentForm,
    AdminCreateCourse,
    AdminAttachModuleToCourse,
    AdminCreateModule,
    AdminCreateTutor,
)
from website.models import (
    Tutor,
    ModuleEnrolment,
    Student,
    Course,
    StudentTutor,
    CourseModule,
    Module,
)

main = Blueprint("main", __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)

    return decorated_function


@main.route("/")
@login_required
def home():
    student_tutors = get_students_for_tutor(current_user.id)
    student_grades = dict()
    for student_tutor in student_tutors:
        id_to_modules = get_student_grades(student_tutor.student_id)
        module_names = []
        module_grades = []

        for id_to_module in id_to_modules.items():
            module_names.append(id_to_module[1].get("module_name"))
            module_grades.append(id_to_module[1].get("module_grade"))
        student_grades[student_tutor.student_id] = {
            "student_name": get_student_name(student_tutor.student_id),
            "module_names": module_names,
            "module_grades": module_grades,
        }
    return render_template(
        "tutor_home.html",
        student_grades=student_grades,
        tutor_name=current_user.tutor_name,
    )


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.tutor_login"))


@main.route("/student/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    form = TutorAddStudentGradeForm()
    success_message = None
    error_message = None
    if form.validate_on_submit():
        if (
            form.module_id.data in get_all_module_ids()
        ) and 0 <= form.grade.data <= 100:
            student_enrolment_module = ModuleEnrolment.query.get(
                (student_id, form.module_id.data)
            )
            if student_enrolment_module is not None:
                student_enrolment_module.grade = form.grade.data
            else:
                db.session.add(
                    ModuleEnrolment(
                        student_id=student_id,
                        module_id=form.module_id.data,
                        grade=form.grade.data,
                        grade_date=datetime.now().date(),
                    )
                )
            db.session.commit()
            form = TutorAddStudentGradeForm(formdata=None)
            success_message = "Completed successfully"
        else:
            error_message = "Module id was not found"
    return render_template(
        "edit_student.html",
        form=form,
        modules=get_all_modules(),
        student_id=student_id,
        student_name=get_student_name(student_id),
        module_enrolments=get_student_enrolments(student_id),
        success_message=success_message,
        error_message=error_message,
    )


@main.route("/course/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_course():
    form = AdminCreateCourse()
    if form.validate_on_submit():
        course = Course(course_name=form.course_name.data)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for("main.edit_course", course_id=course.course_id))
    return render_template("create_course.html", form=form)


@main.route("/course/<int:course_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_course(course_id):
    success_message = None
    error_message = None
    form = AdminAttachModuleToCourse()
    course = Course.query.get(course_id)
    if course is None:
        return redirect(url_for("main.home"))
    if form.validate_on_submit():
        success_message = None
        error_message = None
        if Module.query.get(form.module_id.data) is None:
            error_message = "Module id was not found"
        elif (
            CourseModule.query.filter_by(
                course_id=course_id, module_order=form.module_order.data
            ).first()
            is not None
        ):
            error_message = "The order number was already taken"
        else:
            course_module = CourseModule.query.get((course_id, form.module_id.data))
            if course_module is not None:
                course_module.module_order = form.module_order.data
            else:
                db.session.add(
                    CourseModule(
                        course_id=course_id,
                        module_id=form.module_id.data,
                        module_order=form.module_order.data,
                    )
                )
            db.session.commit()
            success_message = "Completed successfully"
            form = AdminAttachModuleToCourse(formdata=None)
    return render_template(
        "edit_course.html",
        form=form,
        course_id=course_id,
        course_name=course.course_name,
        all_modules=get_all_modules(),
        course_modules=get_modules_for_course(course_id),
        success_message=success_message,
        error_message=error_message,
    )


@main.route("/module/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_module():
    form = AdminCreateModule()
    success_message = None
    if form.validate_on_submit():
        db.session.add(
            Module(
                module_name=form.module_name.data,
            )
        )
        db.session.commit()
        success_message = "Completed successfully"
        form = AdminCreateModule(formdata=None)
    return render_template(
        "create_module.html", form=form, success_message=success_message
    )


@main.route("/tutor/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_tutor():
    form = AdminCreateTutor()
    if form.validate_on_submit():
        if Tutor.query.filter_by(tutor_email=form.tutor_email.data).first() is None:
            db.session.add(
                Tutor(
                    tutor_name=form.tutor_name.data,
                    tutor_email=form.tutor_email.data,
                    tutor_password=bcrypt.generate_password_hash(
                        form.tutor_password.data
                    ),
                    is_admin=form.tutor_is_admin.data,
                )
            )
            db.session.commit()
        return redirect(url_for("main.create_tutor"))
    return render_template("create_tutor.html", form=form)


@main.route("/student/create", methods=["GET", "POST"])
@login_required
def create_student():
    form = TutorCreateStudentForm()
    if form.validate_on_submit():
        if (
            Student.query.filter_by(student_email=form.student_email.data).first()
            is None
            and Course.query.get(form.course_id.data) is not None
        ):
            db.session.add(
                Student(
                    student_email=form.student_email.data,
                    student_name=form.student_name.data,
                    join_date=datetime.now().date(),
                    course_id=form.course_id.data,
                )
            )
            db.session.commit()
            student_id = (
                Student.query.filter_by(student_email=form.student_email.data)
                .first()
                .id
            )
            db.session.add(
                StudentTutor(student_id=student_id, tutor_id=current_user.id)
            )
            db.session.commit()
            return redirect(url_for("main.edit_student", student_id=student_id))
    return render_template(
        "create_student.html",
        form=form,
        courses=get_all_courses(),
    )


@main.route("/login", methods=["GET", "POST"])
def tutor_login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = TutorLoginForm()
    error_message = None
    if form.validate_on_submit():
        user = Tutor.query.filter_by(tutor_email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.tutor_password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("main.home"))
        else:
            error_message = "Incorrect email or password."
    return render_template(
        "tutor_login.html", title="Tutor Login", form=form, error_message=error_message
    )
