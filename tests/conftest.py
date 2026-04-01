import pytest

from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models.course import Course
from app.models.user import User


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

        admin_user = User(
            username="adminuser",
            email="admin@example.com",
            is_admin=True,
        )
        admin_user.set_password("Admin1234")

        normal_user = User(
            username="testuser",
            email="test@example.com",
            is_admin=False,
        )
        normal_user.set_password("Test1234")

        course = Course(
            name="Data Structures",
            code="CSE201",
            description="Test course",
        )

        db.session.add_all([admin_user, normal_user, course])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(client):
    client.post(
        "/login",
        data={
            "email": "test@example.com",
            "password": "Test1234",
        },
        follow_redirects=True,
    )
    return client


@pytest.fixture
def admin_client(client):
    client.post(
        "/login",
        data={
            "email": "admin@example.com",
            "password": "Admin1234",
        },
        follow_redirects=True,
    )
    return client
