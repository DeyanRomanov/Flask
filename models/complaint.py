from sqlalchemy import func

from db import db
from models.enums import State


class ComplaintModel(db.Model):
    __tablename__ = 'complaint'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, server_default=func.now())
    status = db.Column(db.Enum(State), nullable=False, default=State.pending)
    complainer_id = db.Column(db.Integer, db.ForeignKey('complainer.id'), nullable=False)
    complainer = db.relationship('ComplainerModel')
