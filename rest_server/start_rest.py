#!/usr/bin/python3
from app import app, db
from app import routes
from app.models.client import Client
from app.models.dataset import Dataset

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
