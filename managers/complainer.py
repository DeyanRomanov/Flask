from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager
from models import ComplainerModel


class ComplainerManager:
    @staticmethod
    def register(complainer_data):
        complainer_data['password'] = generate_password_hash(complainer_data['password'])
        user = ComplainerModel(**complainer_data)
        db.session.add(user)
        db.session.commit()
        return AuthManager.encode_token(user)

    @staticmethod
    def login(login_data):
        complainer = ComplainerModel.query.filter_by(email=login_data['email']).first()
        if complainer and login_data['password']:
            if check_password_hash(complainer.password, login_data['password']):
                return AuthManager.encode_token(complainer)

        raise BadRequest('No such email or password!')
