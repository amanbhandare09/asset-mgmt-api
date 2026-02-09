from flask import Flask
from .config import Config
from .extensions import db, jwt, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import models for migration detection
    from .models import User, CashbackAsset, CashbackClaimLedger

    @app.route("/")
    def home():
        return {"message": "Asset Management API Running"}

    return app
