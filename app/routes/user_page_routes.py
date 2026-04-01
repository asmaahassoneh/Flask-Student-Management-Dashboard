from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError

from app.models.user import User
from app.services.user_service import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_id,
    update_user,
)
from app.utils.decorators import admin_required
from app.utils.validators import normalize_email, normalize_text, validate_user_form

user_page_bp = Blueprint("user_page_bp", __name__, url_prefix="/users")


@user_page_bp.route("")
@login_required
@admin_required
def list_users():
    users = get_all_users()
    return render_template("users.html", users=users)


@user_page_bp.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_user():
    form_data = {
        "username": "",
        "email": "",
    }

    if request.method == "GET":
        return render_template("add_user.html", error=None, form_data=form_data)

    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    form_data = {
        "username": username,
        "email": email,
    }

    error = validate_user_form(username, email, password, confirm_password)
    if error:
        return render_template("add_user.html", error=error, form_data=form_data)

    existing_username = User.query.filter_by(username=normalize_text(username)).first()
    if existing_username:
        return render_template(
            "add_user.html",
            error="Username already exists.",
            form_data=form_data,
        )

    existing_email = User.query.filter_by(email=normalize_email(email)).first()
    if existing_email:
        return render_template(
            "add_user.html",
            error="Email already exists.",
            form_data=form_data,
        )

    try:
        create_user(
            {
                "username": username,
                "email": email,
                "password": password,
            }
        )
        flash("User added successfully.", "success")
        return redirect(url_for("user_page_bp.list_users"))
    except SQLAlchemyError:
        return render_template(
            "add_user.html",
            error="Database error occurred.",
            form_data=form_data,
        )


@user_page_bp.route("/<int:user_id>")
@login_required
@admin_required
def user_details(user_id):
    user = get_user_by_id(user_id)

    if user is None:
        abort(404)

    return render_template("user_details.html", user=user)


@user_page_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        abort(404)

    if request.method == "GET":
        return render_template("edit_user.html", user=user, error=None)

    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    error = validate_user_form(username, email, password=password, partial=True)
    if error:
        return render_template("edit_user.html", user=user, error=error)

    existing_username = User.query.filter_by(username=normalize_text(username)).first()
    if existing_username and existing_username.id != user.id:
        return render_template(
            "edit_user.html",
            user=user,
            error="Username already exists.",
        )

    existing_email = User.query.filter_by(email=normalize_email(email)).first()
    if existing_email and existing_email.id != user.id:
        return render_template(
            "edit_user.html",
            user=user,
            error="Email already exists.",
        )

    data = {
        "username": username,
        "email": email,
    }

    if password:
        data["password"] = password

    try:
        update_user(user, data)
        flash("User updated successfully.", "success")
        return redirect(url_for("user_page_bp.user_details", user_id=user.id))
    except SQLAlchemyError:
        return render_template(
            "edit_user.html",
            user=user,
            error="Database error occurred.",
        )


@user_page_bp.route("/<int:user_id>/delete", methods=["POST"])
@login_required
@admin_required
def remove_user(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        abort(404)

    try:
        delete_user(user)
        flash("User deleted successfully.", "success")
    except SQLAlchemyError:
        flash("Something went wrong while deleting the user.", "error")

    return redirect(url_for("user_page_bp.list_users"))
