from app.extensions import db
from app.models.user import User
from app.utils.validators import normalize_email, normalize_text


def get_all_users():
    return User.query.order_by(User.username.asc()).all()


def get_user_by_id(user_id):
    return db.session.get(User, user_id)


def create_user(data):
    user = User(
        username=normalize_text(data["username"]),
        email=normalize_email(data["email"]),
        is_admin=data.get("is_admin", False),
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()
    return user


def update_user(user, data):
    if "username" in data:
        user.username = normalize_text(data["username"])

    if "email" in data:
        user.email = normalize_email(data["email"])

    if "password" in data and data["password"]:
        user.set_password(data["password"])

    db.session.commit()
    return user


def delete_user(user):
    db.session.delete(user)
    db.session.commit()
