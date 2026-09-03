from datetime import datetime, timedelta, timezone
import jwt
from app.config.settings import settings

def create_access_token(user_id: str, role: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {
        "sub": user_id,
        "role": role,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return token