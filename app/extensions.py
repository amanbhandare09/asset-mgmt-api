from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Database instance
db = SQLAlchemy()

# JWT instance
jwt = JWTManager()

# Migration engine
migrate = Migrate()

limiter = Limiter(
    key_func=get_remote_address
)