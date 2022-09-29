import jwt

from datetime import datetime, timedelta
from decouple import config


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {"sub": user.id, "exp": datetime.utcnow() + timedelta(minutes=30)}
        return jwt.encode(payload, key=config('SECRET_KEY'), algorithm='HS256')
