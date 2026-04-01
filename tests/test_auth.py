from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.user import User


def create_user(
    app,
    username="asmaa",
    email="asmaa@example.com",
    password="asmaa123",
    is_admin=False,
):
    with app.app_context():
        existing_user = User.query.filter_by(email=email).first()
        if existing_user is None:
            user = User(username=username, email=email, is_admin=is_admin)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_register_page_loads(client):
    response = client.get("/register")
    assert response.status_code == 200


def test_register_success(client, app):
    response = client.post(
        "/register",
        data={
            "username": "asmaa",
            "email": "asmaa@example.com",
            "password": "asmaa123",
            "confirm_password": "asmaa123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Registration successful" in response.data

    with app.app_context():
        user = User.query.filter_by(email="asmaa@example.com").first()
        assert user is not None
        assert user.username == "asmaa"


def test_register_passwords_do_not_match(client):
    response = client.post(
        "/register",
        data={
            "username": "asmaa",
            "email": "asmaa@example.com",
            "password": "asmaa123",
            "confirm_password": "pass1234",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Passwords do not match." in response.data


def test_register_missing_fields(client):
    response = client.post(
        "/register",
        data={
            "username": "",
            "email": "",
            "password": "",
            "confirm_password": "",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"All fields are required." in response.data


def test_register_invalid_email_format(client):
    response = client.post(
        "/register",
        data={
            "username": "asmaa",
            "email": "not-an-email",
            "password": "asmaa123",
            "confirm_password": "asmaa123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Email is not valid." in response.data


def test_register_duplicate_user(client, app):
    create_user(app)

    response = client.post(
        "/register",
        data={
            "username": "asmaa",
            "email": "asmaa@example.com",
            "password": "asmaa123",
            "confirm_password": "asmaa123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Username or email already exists." in response.data


def test_register_database_error(client, monkeypatch):
    def broken_commit():
        raise SQLAlchemyError("Database failed")

    monkeypatch.setattr("app.routes.auth_routes.db.session.commit", broken_commit)

    response = client.post(
        "/register",
        data={
            "username": "asmaa",
            "email": "asmaa@example.com",
            "password": "asmaa123",
            "confirm_password": "asmaa123",
        },
        follow_redirects=False,
    )

    assert response.status_code == 500
    assert b"Something went wrong while creating your account." in response.data


def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_login_success(client, app):
    create_user(app)

    response = client.post(
        "/login",
        data={
            "email": "asmaa@example.com",
            "password": "asmaa123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Login successful." in response.data
    assert b"Welcome, asmaa!" in response.data


def test_login_invalid_credentials(client, app):
    create_user(app)

    response = client.post(
        "/login",
        data={
            "email": "asmaa@example.com",
            "password": "wrongpass123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid email or password." in response.data


def test_login_invalid_email_format(client):
    response = client.post(
        "/login",
        data={
            "email": "not-an-email",
            "password": "asmaa123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Email is not valid." in response.data


def test_login_missing_fields(client):
    response = client.post(
        "/login",
        data={
            "email": "",
            "password": "",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Email and password are required." in response.data


def test_dashboard_requires_login(client):
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page." in response.data


def test_dashboard_access_after_login(client, app):
    create_user(app)

    client.post(
        "/login",
        data={
            "email": "asmaa@example.com",
            "password": "asmaa123",
        },
        follow_redirects=True,
    )

    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b"Welcome, asmaa!" in response.data


def test_logout(client, app):
    create_user(app)

    client.post(
        "/login",
        data={"email": "asmaa@example.com", "password": "asmaa123"},
        follow_redirects=True,
    )

    response = client.post("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Logged out successfully." in response.data


def test_logout_requires_login(client):
    response = client.post("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page." in response.data


def test_404_page_html(client):
    response = client.get("/this-page-does-not-exist")
    assert response.status_code == 404


def test_403_page_html(auth_client):
    response = auth_client.get("/users", follow_redirects=False)
    assert response.status_code == 403
