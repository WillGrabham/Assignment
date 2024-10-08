from datetime import datetime
from functools import wraps

from flask import redirect, render_template, url_for, Blueprint, flash
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
    get_student_course,
)
from website.forms import (
    TutorLoginForm,
    TutorAddStudentGradeForm,
    TutorCreateStudentForm,
    AdminCreateCourse,
    AdminAttachModuleToCourse,
    AdminCreateModule,
    AdminCreateTutor,
    TutorChangeStudentCourseForm,
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
    students = get_students_for_tutor(current_user.id)
    student_grades = dict()
    for student in students:
        module_id_to_enrolment = get_student_grades(student.student_id)
        module_names = []
        module_grades = []
        # Iterate over student's enrolments, adding module name and grade to separate lists
        for id_to_module in module_id_to_enrolment.items():
            module_names.append(id_to_module[1].get("module_name"))
            module_grades.append(id_to_module[1].get("module_grade"))
        # Add student's grades to dictionary
        student_grades[student.student_id] = {
            "student_name": get_student_name(student.student_id),
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
        # validate inputs server-side, and module is correct
        if (
            form.module_id.data in get_all_module_ids()
        ) and 0 <= form.grade.data <= 100:
            student_enrolment_module = ModuleEnrolment.query.get(
                (student_id, form.module_id.data)
            )
            # if student is already enrolled on module, just update grade. Otherwise, create new module enrolment
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
            # Add to database, reset form to blank, display success_message on re-render
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
        student_course=get_student_course(student_id),
        module_enrolments=get_student_enrolments(student_id),
        success_message=success_message,
        error_message=error_message,
    )


@main.route("/student/<int:student_id>/course", methods=["GET", "POST"])
@login_required
def edit_student_course(student_id):
    error_message = None
    form = TutorChangeStudentCourseForm()
    if form.validate_on_submit():
        # Checks course id is valid
        if Course.query.get(form.course_id.data) is None:
            error_message = "Course does not exist"
        else:
            # updates student's course id
            student = Student.query.get(student_id)
            student.course_id = form.course_id.data
            db.session.commit()
            return redirect(url_for("main.edit_student", student_id=student.id))
    return render_template(
        "edit_student_course.html",
        form=form,
        student_name=get_student_name(student_id),
        student_course=get_student_course(student_id),
        error_message=error_message,
        courses=get_all_courses(),
        student_id=student_id,
    )


@main.route("/course/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_course():
    form = AdminCreateCourse()
    if form.validate_on_submit():
        # creates course, adds to database, redirects to the course's edit page for tutor to add modules
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
        # checks module_id matches to a module, and order number isn't taken
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
            # uses composite primary key to find if module is already attached to course - if it is, just update order
            course_module = CourseModule.query.get((course_id, form.module_id.data))
            if course_module is not None:
                course_module.module_order = form.module_order.data
            else:
                # otherwise attach module to course
                db.session.add(
                    CourseModule(
                        course_id=course_id,
                        module_id=form.module_id.data,
                        module_order=form.module_order.data,
                    )
                )
            # Add to database, reset form to blank, display success_message on re-render
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
        # create new module, insert into database, re-render same page with empty form and success message
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
    error_message = None
    if form.validate_on_submit():
        # checks tutor email is not already used then add new tutor to database, otherwise show error message
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
        else:
            error_message = "Tutor email is already in use"
    return render_template("create_tutor.html", form=form, error_message=error_message)


@main.route("/student/create", methods=["GET", "POST"])
@login_required
def create_student():
    form = TutorCreateStudentForm()
    error_message = None
    if form.validate_on_submit():
        # checks student email is not already used
        if (
            Student.query.filter_by(student_email=form.student_email.data).first()
            is None
        ):
            # checks course id relates to a course
            if Course.query.get(form.course_id.data) is not None:
                # add student to database
                db.session.add(
                    Student(
                        student_email=form.student_email.data,
                        student_name=form.student_name.data,
                        join_date=datetime.now().date(),
                        course_id=form.course_id.data,
                    )
                )
                db.session.commit()
                # get created student and create relationship to the tutor who is creating it
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
            else:
                error_message = "Course was not found"
        else:
            error_message = "Student email is not unique"
    return render_template(
        "create_student.html",
        form=form,
        courses=get_all_courses(),
        error_message=error_message,
    )


@main.route("/tutors", methods=["GET", "POST"])
@login_required
@admin_required
def view_tutors():
    # display list of tutors
    return render_template("tutor_view.html", tutors=Tutor.query.all())


@main.route("/tutor/<int:tutor_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_tutor(tutor_id):
    # this is a POST request, so we must use flashes for errors
    # checks tutor is a valid tutor, and the tutor isn't themselves (otherwise you can end up with no admins)
    tutor = Tutor.query.get(tutor_id)
    if tutor is None:
        flash("Tutor could not be deleted, please try again", "error")
    elif tutor == current_user:
        flash("You cannot delete your own account", "error")
    else:
        db.session.delete(tutor)
        db.session.commit()
        flash("Tutor deleted successfully", "success")
    return redirect(url_for("main.view_tutors"))


@main.route("/login", methods=["GET", "POST"])
def tutor_login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = TutorLoginForm()
    error_message = None
    if form.validate_on_submit():
        # check email matches a tutor's email, and hashed password matches
        user = Tutor.query.filter_by(tutor_email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.tutor_password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("main.home"))
        else:
            error_message = "Incorrect email or password."
    return render_template(
        "tutor_login.html", title="Tutor Login", form=form, error_message=error_message
    )
