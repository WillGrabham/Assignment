from app import create_app, db
from app.models import Student

app = create_app()

with app.app_context():
    db.create_all()
    student = Student(name="Some Name")
    db.session.add(student)
    db.session.commit()
