from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from db import db
from resources.routes import routes

app = Flask(__name__)
db.init_app(app)
app.config.from_object("config.DevelopmentConfig")
api = Api(app)
migrate = Migrate(app, db)

[api.add_resource(*route) for route in routes]

if __name__ == '__main__':
    app.run()
