from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models import State


class ComplaintSchemaResponse(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    amount = fields.Float()
    created_on = fields.DateTime()
    photo_url = fields.String()
    status = EnumField(State, by_value=True)
    # complainer = fields.Nested()
