from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

# Database instance
db = SQLAlchemy()

# JWT instance
jwt = JWTManager()

# Migration engine
migrate = Migrate()

limiter = Limiter(
    key_func=get_remote_address
)

try:

    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True
    )

    redis_client.ping()
    REDIS_AVAILABLE = True

except Exception:

    redis_client = None
    REDIS_AVAILABLE = False
