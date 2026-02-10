from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.extensions import REDIS_AVAILABLE


storage = (
    "redis://localhost:6379"
    if REDIS_AVAILABLE
    else "memory://"
)

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=storage
)
