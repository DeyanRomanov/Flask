import jwt

from datetime import datetime, timedelta
from decouple import config
from flask_httpauth import HTTPTokenAuth
from jwt import ExpiredSignatureError, InvalidTokenError
from werkzeug.exceptions import BadRequest

from models import ComplainerModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {"sub": user.id, "exp": datetime.utcnow() + timedelta(minutes=30)}
        return jwt.encode(payload, key=config('SECRET_KEY'), algorithm='HS256')

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, key=config('SECRET_KEY'), algorithms=['HS256'])
            return payload["sub"]
        except ExpiredSignatureError:
            raise BadRequest("Token expired")
        except InvalidTokenError:
            raise BadRequest("Invalid token")


auth = HTTPTokenAuth()


@auth.verify_token
def verify(token):
    user_id = AuthManager.decode_token(token)
    return ComplainerModel.query.filter_by(id=user_id).first()
