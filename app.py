# import enum
# from datetime import datetime, timedelta
#
# import jwt
# from functools import wraps
#
# from decouple import config
# from flask import Flask, request
# from flask_migrate import Migrate
# from flask_restful import Api, Resource, abort
# from flask_sqlalchemy import SQLAlchemy
# from jwt import InvalidSignatureError, ExpiredSignatureError
# from marshmallow_enum import EnumField
# from password_strength import PasswordPolicy
# from sqlalchemy import func
# from marshmallow import Schema, fields, ValidationError, validate, validates
# from werkzeug.exceptions import BadRequest, Forbidden
# from werkzeug.security import generate_password_hash
# from flask_httpauth import HTTPTokenAuth
#
# app = Flask(__name__)
#
# db_user = config('DB_USER')
# db_password = config('DB_PASSWORD')
# db_name = config('DB_NAME')
# db_port = config('DB_PORT')
# db_host = config('DB_HOST')
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
# db = SQLAlchemy(app)
# api = Api(app)
# migrate = Migrate(app, db)
#
# auth = HTTPTokenAuth(scheme="Bearer")
#
#
# @auth.verify_token
# def verify_token(token):
#     try:
#         data = jwt.decode(token, key=config('SECRET_KEY'), algorithms=['HS256'])
#         user_id = data["sub"]
#         user = User.query.filter_by(id=user_id).first()
#         if user:
#             return user
#     except InvalidSignatureError:
#         raise BadRequest('Invalid token!')
#     except ExpiredSignatureError:
#         raise BadRequest('Expired token!')
#     except Exception as ex:
#         raise ex
#
#
# class ColorEnum(enum.Enum):
#     pink = "pink"
#     black = "black"
#     white = "white"
#     yellow = "yellow"
#
#
# class SizeEnum(enum.Enum):
#     xs = "xs"
#     s = "s"
#     m = "m"
#     l = "l"
#     xl = "xl"
#     xxl = "xxl"
#
#
# class UserRoleEnum(enum.Enum):
#     user = 'User'
#     admin = 'Admin'
#     super_admin = 'Super Admin'
#
#
# user_clothes = db.Table(
#     "user_clothes",
#     db.Model.metadata,
#     db.Column("id", db.Integer, primary_key=True, autoincrement=True),
#     db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
#     db.Column("clothes_id", db.Integer, db.ForeignKey("clothes.id")),
# )
#
# policy = PasswordPolicy.from_names(
#     uppercase=1,
#     numbers=1,
#     special=1,
#     nonletters=1,
# )
#
#
# def validate_schema(schema_name):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             schema = schema_name()
#             errors = schema.validate(request.get_json())
#             if errors:
#                 abort(400, errors=errors)
#             return f(*args, **kwargs)
#
#         return decorated_function
#
#     return decorator
#
#
# def permission_required(role_name):
#     def decorator(func):
#         def decorated_func(*args, **kwargs):
#             current_user = auth.current_user()
#             if current_user.role == role_name:
#                 return func(*args, **kwargs)
#             raise Forbidden("You do not permissions to access!")
#
#         return decorated_func
#
#     return decorator
#
#
# class UserSignInSchema(Schema):
#     email = fields.Email(required=True,
#                          )
#     password = fields.Str(
#         required=True,
#     )
#     full_name = fields.Str(
#         required=True,
#         validate=validate.And(validate.Length(max=255))
#     )
#
#     @validates('full_name')
#     def validate_full_name_fields(self, name):
#         try:
#             first_name, last_name = name.split()
#         except ValueError:
#             raise ValidationError("First and last name are mandatory")
#
#         if len(first_name) < 3 or len(last_name) < 3:
#             raise ValidationError("Each name should contain at least 3 chars")
#
#     @validates('password')
#     def validate_password(self, password):
#         errors = policy.test(password)
#         if errors:
#             raise ValidationError("Password does not meet requirements")
#
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), nullable=False, unique=True)
#     password = db.Column(db.String(255), nullable=False)
#     full_name = db.Column(db.String(255), nullable=False)
#     phone = db.Column(db.Text)
#     create_on = db.Column(db.DateTime, server_default=func.now())
#     updated_on = db.Column(db.DateTime, onupdate=func.now())
#     clothes = db.relationship("Clothes", secondary=user_clothes)
#     role = db.Column(db.Enum(UserRoleEnum), server_default=UserRoleEnum.user.name, nullable=False)
#
#     def encode_token(self):
#         payload = {"exp": datetime.utcnow() + timedelta(days=1), "sub": self.id}
#         try:
#             return jwt.encode(payload, key=config("SECRET_KEY"), algorithm="HS256")
#         except Exception as ex:
#             raise ex
#
#
# class Clothes(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     color = db.Column(db.Enum(ColorEnum), default=ColorEnum.white, nullable=False)
#     size = db.Column(db.Enum(SizeEnum), default=SizeEnum.s, nullable=False)
#     photo = db.Column(db.String(255), nullable=False)
#     create_on = db.Column(db.DateTime, server_default=func.now())
#     updated_on = db.Column(db.DateTime, onupdate=func.now())
#
#
# class UserSignIn(Resource):
#     @validate_schema(UserSignInSchema)
#     def post(self):
#         data = request.get_json()
#         data['password'] = generate_password_hash(data['password'])
#         user = User(**data)
#         db.session.add(user)
#         db.session.commit()
#         token = user.encode_token()
#         return {"token": token}, 201
#
#
# class ClothesSchema(Schema):
#     id = fields.Integer()
#     name = fields.Str()
#     color = EnumField(ColorEnum, by_value=True)
#     size = EnumField(SizeEnum, by_value=True)
#     create_on = fields.DateTime()
#
#
# class UserResponseSchema(Schema):
#     id = fields.Integer()
#     full_name = fields.Str()
#     clothes = fields.List(fiaelds.Nested(ClothesSchema), many=True)
#
#
# class UserResource(Resource):
#     def get(self, pk):
#         user = User.query.filter_by(id=pk).first()
#         return UserResponseSchema().dump(user)
#
#
# class ClothesRouter(Resource):
#     @auth.login_required
#     @permission_required(UserRoleEnum.user)
#     def get(self):
#         return UserResponseSchema().dump(auth.current_user())
#
#
# api.add_resource(UserSignIn, '/register/')
# api.add_resource(UserResource, '/user/<int:pk>/')
# api.add_resource(ClothesRouter, '/clothes/')
#
# if __name__ == "__main__":
#     app.run(debug=True)
#
#
# class BaseUser(db.Model):
#     username = db.Column()