from app import create_app
from app.extensions import db
from app.models.course import Course
from app.models.student import Student
from app.models.user import User

app = create_app()


def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin = User(
            username="admin",
            email="admin@gmail.com",
            is_admin=True,
        )
        admin.set_password("Admin123")

        user = User(username="asmaa", email="asmaa@example.com", is_admin=False)
        user.set_password("Asmaa123")

        course1 = Course(
            name="Data Structures", code="CSE201", description="Core CS course"
        )
        course2 = Course(
            name="Digital Logic Design",
            code="CPE210",
            description="Logic gates and circuits",
        )
        course3 = Course(
            name="Computer Architecture",
            code="CPE320",
            description="CPU and memory design",
        )
        course4 = Course(
            name="Microprocessors", code="CPE330", description="Processor systems"
        )
        course5 = Course(
            name="Signals and Systems", code="CPE340", description="Signals basics"
        )
        course6 = Course(
            name="Image Processing", code="CPE450", description="Digital image analysis"
        )

        student1 = Student(
            name="Asmaa Hassoneh",
            student_id="12112458",
        )
        student1.courses.extend([course1, course2, course6])

        student2 = Student(
            name="Lina Ahmad",
            student_id="12112459",
        )
        student2.courses.extend([course1, course3])

        student3 = Student(
            name="Omar Khaled",
            student_id="12112460",
        )
        student3.courses.extend([course4, course5])

        db.session.add_all(
            [
                admin,
                user,
                course1,
                course2,
                course3,
                course4,
                course5,
                course6,
                student1,
                student2,
                student3,
            ]
        )
        db.session.commit()

        print("Database seeded successfully.")


if __name__ == "__main__":
    seed_data()
