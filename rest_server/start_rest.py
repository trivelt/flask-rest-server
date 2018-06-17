#!/usr/bin/python3
from app import db, create_production_app
from app.routes import configure_routes
import argparse


def import_models():
    from app.models.client import Client
    from app.models.dataset import Dataset


def prepare_app(api):
    import_models()
    configure_routes(api)
    db.create_all()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='specify input config file for Flask Rest API server', type=str)

    args = parser.parse_args()
    return args.config


if __name__ == "__main__":
    config_file = parse_arguments()
    app, api = create_production_app(config_file)
    prepare_app(api)
    app.run()
