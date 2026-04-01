from functools import wraps

from flask import abort, jsonify, request
from flask_login import current_user


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.path.startswith("/api/"):
                return (
                    jsonify({"success": False, "error": "Authentication required."}),
                    401,
                )
            abort(401)

        if not current_user.is_admin:
            if request.path.startswith("/api/"):
                return (
                    jsonify({"success": False, "error": "Admin access required."}),
                    403,
                )
            abort(403)

        return view_func(*args, **kwargs)

    return wrapper
