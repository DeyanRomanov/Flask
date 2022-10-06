from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth import auth


def validate_schema(schema_name):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            schema = schema_name()
            errors = schema.validate(data)
            if errors:
                raise BadRequest(errors)

            return func(*args, **kwargs)

        return wrapper

    return decorated_function


def permission_required(role):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            if current_user.role == role:
                return func(*args, **kwargs)
            raise Forbidden("Permission denied")

        return wrapper

    return decorated_function
