from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_test_app():
    app = Flask("RestAPI Test Server")
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/testdb.sqlite"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()
    api = Api(app)
    return app, api


def create_production_app():
    app = Flask("RestAPI Server")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/rest_db.sqlite"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()
    api = Api(app)
    return app, api
