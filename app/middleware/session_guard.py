from functools import wraps
from flask import session, redirect


def login_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect("/auth/login-page")

        return fn(*args, **kwargs)

    return wrapper

