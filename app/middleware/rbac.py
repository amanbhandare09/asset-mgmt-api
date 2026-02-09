from functools import wraps
from flask import session, redirect, jsonify


def admin_required(fn):
    """
    RBAC Guard — Allows only ADMIN role users.

    Works with session-based authentication.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):

        # Check login first
        if "user_id" not in session:
            return redirect("/auth/login-page")

        # Role check
        role = session.get("role")

        if role != "ADMIN":
            return jsonify({
                "error": "Admin access required"
            }), 403

        return fn(*args, **kwargs)

    return wrapper
