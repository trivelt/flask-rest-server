from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("RestAPI Server")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/rest_db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
