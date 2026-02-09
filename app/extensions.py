from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Database instance
db = SQLAlchemy()

# JWT instance
jwt = JWTManager()

# Migration engine
migrate = Migrate()
