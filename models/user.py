from db import db
from models.enums import UserRole


class BaseUserModel(db.Model):
    __tablename__ = 'base_user'
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True, unique=True)
    phone = db.Column(db.String(14), nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=True)


class ComplainerModel(BaseUserModel):
    __tablename__ = 'complainer'
    role = db.Column(
        db.Enum(UserRole),
        default=UserRole.complainer,
        nullable=False
    )
    complains = db.relationship('ComplaintModel', backref='complaint', lazy='dynamic')


class ApproverModel(BaseUserModel):
    __tablemodel__ = 'approver'

    role = db.Column(
        db.Enum(UserRole),
        default=UserRole.approver,
        nullable=False,
    )


class AdminModel(BaseUserModel):
    __tablename__ = 'admin'

    role = db.Column(
        db.Enum(UserRole),
        default=UserRole.admin,
        nullable=False,
    )
