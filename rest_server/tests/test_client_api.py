import unittest
from app import create_test_app, db
from app.models.client import Client
from start_rest import prepare_app
from flask_api import status


class TestClientApi(unittest.TestCase):
    def setUp(self):
        self.app, api = create_test_app()
        self.client = self.app.test_client()
        prepare_app(api)

    def tearDown(self):
        db.drop_all()
        self.app.app_context().push()

    def test_something(self):
        pass