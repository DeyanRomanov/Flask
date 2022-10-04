from marshmallow import Schema, validate, fields


class AuthBase(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
