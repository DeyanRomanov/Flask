from marshmallow import fields, validate

from schemas.requests.base import AuthBase


class RegisterSchemaRequest(AuthBase):
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=24))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=24))
    phone = fields.String(required=True, validate=validate.Length(min=14, max=14))


class LoginSchemaRequest(AuthBase):
    pass
