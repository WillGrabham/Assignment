from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired, Email, NumberRange


class TutorLoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class TutorAddStudentGradeForm(FlaskForm):
    module_id = IntegerField("Module id", validators=[DataRequired()])
    grade = IntegerField(
        "Grade", validators=[DataRequired(), NumberRange(min=0, max=100)]
    )
    submit = SubmitField("Add Grade")


class TutorChangeStudentCourseForm(FlaskForm):
    course_id = IntegerField("Course id", validators=[DataRequired()])
    submit = SubmitField("Change Course")


class TutorCreateStudentForm(FlaskForm):
    student_email = EmailField("Email", validators=[DataRequired(), Email()])
    student_name = StringField("Name", validators=[DataRequired()])
    course_id = IntegerField("Course id", validators=[DataRequired()])
    submit = SubmitField("Create student")


class AdminCreateCourse(FlaskForm):
    course_name = StringField("Course name", validators=[DataRequired()])


class AdminAttachModuleToCourse(FlaskForm):
    module_id = IntegerField("Module id", validators=[DataRequired()])
    module_order = IntegerField(
        "Module order", validators=[DataRequired(), NumberRange(min=0)]
    )


class AdminCreateModule(FlaskForm):
    module_name = StringField("Module name", validators=[DataRequired()])


class AdminCreateTutor(FlaskForm):
    tutor_name = StringField("Name", validators=[DataRequired()])
    tutor_email = EmailField("Email", validators=[DataRequired(), Email()])
    tutor_password = PasswordField("Password", validators=[DataRequired()])
    tutor_is_admin = BooleanField("Is Admin")
