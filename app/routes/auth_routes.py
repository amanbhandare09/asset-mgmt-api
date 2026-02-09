from flask import Blueprint, request, session, render_template
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User
import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    hashed_pw = bcrypt.hashpw(
        data["password"].encode(),
        bcrypt.gensalt()
    ).decode()

    user = User(
        email=data["email"],
        password_hash=hashed_pw
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "Registered"}

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    user = User.query.filter_by(
        email=data["email"]
    ).first()

    if not user:
        return {"error": "Invalid credentials"}, 401

    if not bcrypt.checkpw(
        data["password"].encode(),
        user.password_hash.encode()
    ):
        return {"error": "Invalid credentials"}, 401

    # JWT for APIs
    token = create_access_token(
        identity=str(user.id)
    )

    # SESSION for UI
    session["user_id"] = user.id
    session["role"] = user.role

    return {
        "access_token": token,
        "role": user.role
    }

@auth_bp.route("/logout")
def logout():

    session.clear()
    return {"message": "Logged out"}

@auth_bp.route("/login-page")
def login_page():
    return render_template("auth/login.html")


@auth_bp.route("/register-page")
def register_page():
    return render_template("auth/register.html")
