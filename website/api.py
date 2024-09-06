from website.models import Student, StudentTutor, ModuleEnrolment, CourseModule, Module, Course


def get_students_for_tutor(tutor_id):
    return StudentTutor.query.filter_by(tutor_id=tutor_id).all()


def get_student_grades(student_id):
    enrolled_course_id = Student.query.get(student_id).course_id
    print("enrolled_course_id", enrolled_course_id)
    valid_course_modules = CourseModule.query.filter_by(course_id=enrolled_course_id).all()
    print("valid_course_modules", valid_course_modules)
    valid_course_module_ids = []
    for valid_course_module in valid_course_modules:
        valid_course_module_ids.append(valid_course_module.module_id)
    print("valid_course_module_ids", valid_course_module_ids)
    all_enrolments = ModuleEnrolment.query.filter_by(student_id=student_id).all()
    print("all_enrolments", all_enrolments)
    filtered_grades = dict()
    for enrolment in all_enrolments:
        if enrolment.module_id in valid_course_module_ids:
            filtered_grades[enrolment.module_id] = {
                'module_grade': enrolment.grade,
                'module_name': Module.query.get(enrolment.module_id).module_name,
            }
    print(filtered_grades)
    return filtered_grades


def get_all_modules():
    return Module.query.all()


def get_all_courses():
    return Course.query.all()


def get_all_module_ids():
    modules = get_all_modules()
    module_ids = []
    for module in modules:
        module_ids.append(module.module_id)
    return module_ids


def get_student_enrolments(student_id):
    return ModuleEnrolment.query.filter_by(student_id=student_id).all()


def get_student_name(student_id):
    return Student.query.get(student_id).student_name
