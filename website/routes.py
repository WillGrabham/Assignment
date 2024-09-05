from flask import redirect, render_template, url_for, Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from website import bcrypt
from website.api import get_student_grades, get_student_name, get_students_for_tutor
from website.forms import TutorLoginForm
from website.models import Tutor

main = Blueprint('main', __name__)


def is_tutor():
    return Tutor.query.filter_by(id=current_user.id).first() is not None

@main.route('/')
@login_required
def home():
    if is_tutor():
        student_tutors = get_students_for_tutor(current_user.id)
        student_grades = dict()
        for student_tutor in student_tutors:
            id_to_modules = get_student_grades(student_tutor.student_id)
            module_names = []
            module_grades = []

            for id_to_module in id_to_modules.items():
                module_names.append(id_to_module[1].get('module_name'))
                module_grades.append(id_to_module[1].get('module_grade'))
            print(module_names)
            student_grades[student_tutor.student_id] = {
                'student_name': get_student_name(student_tutor.student_id),
                'module_names': module_names,
                'module_grades': module_grades
            }
        print(student_grades)
        return render_template("tutor_home.html", student_grades=student_grades)
    else:
        return render_template("index.html")


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@main.route('/tutor/login', methods=['GET', 'POST'])
def tutor_login():
    print('in tutor login')
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = TutorLoginForm()
    if form.validate_on_submit():
        print('is submitted');
        user = Tutor.query.filter_by(tutor_email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.tutor_password, form.password.data):
            login_user(user, remember=form.remember.data)
            print('user is valid')
            return redirect(url_for('main.home'))
    return render_template('tutor_login.html', title='Tutor Login', form=form)
