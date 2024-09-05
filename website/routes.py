from flask import redirect, render_template, url_for, Blueprint
from flask_login import current_user, login_user

from website import bcrypt
from website.forms import TutorLoginForm
from website.models import Tutor

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template("index.html")


@main.route('/tutor/login', methods=['GET', 'POST'])
def tutor_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = TutorLoginForm()
    if form.validate_on_submit():
        user = Tutor.query.filter_by(tutor_email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.tutor_password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
    return render_template('tutor_login.html', title='Tutor Login', form=form)
