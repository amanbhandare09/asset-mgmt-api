from flask import Flask
from .config import Config
from .extensions import db, jwt, migrate
from app.utils.limiter import limiter
from app.scheduler import start_scheduler


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # Session secret
    app.secret_key = app.config["SECRET_KEY"]

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)


    # Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.cashback_routes import cashback_bp
    from .routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cashback_bp, url_prefix="/cashback")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from flask import session

    @app.context_processor
    def inject_user():

        return dict(
            role=session.get("role"),
            email=session.get("email"),
            logged_in=("user_id" in session)
        )

    start_scheduler(app)

    @app.template_filter("datetime_local")
    def format_datetime_local(value):
        return value.strftime("%Y-%m-%dT%H:%M")

    # Landing page
    from flask import render_template

    @app.route("/")
    def landing():
        return render_template("landing.html")

    return app
