from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange


class TutorLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class TutorAddStudentGradeForm(FlaskForm):
    module_id = IntegerField('Module id', validators=[DataRequired()])
    grade = IntegerField('Grade', validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Add Grade')
