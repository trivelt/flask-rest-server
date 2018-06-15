#!/usr/bin/python3
from app import db, create_production_app
from app.routes import configure_routes


def import_models():
    from app.models.client import Client
    from app.models.dataset import Dataset


def prepare_app(api):
    import_models()
    configure_routes(api)
    db.create_all()

if __name__ == "__main__":
    app, api = create_production_app()
    prepare_app(api)
    app.run(debug=True)
