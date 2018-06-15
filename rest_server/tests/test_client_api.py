import unittest
from app import create_test_app, db
from app.models.client import Client
from tests.tests_utils import *
from start_rest import prepare_app
from flask_api import status
import json


class TestClientApi(unittest.TestCase):
    def setUp(self):
        self.app, api = create_test_app()
        self.client = self.app.test_client()
        prepare_app(api)

    def tearDown(self):
        db.drop_all()
        self.app.app_context().push()

    def test_cannot_patch_nonexistent_client(self):
        response = self.client.patch('/clients/10', data=json.dumps({'name': 'Client', 'ip_address': 'localhost'}),
                                     content_type='application/json')
        assert_status_code_equal(response, status.HTTP_400_BAD_REQUEST)

    def test_patch_client_correctly(self):
        client_id = 1
        new_name = "NewClient"

        response = self.client.post('/clients', data=json.dumps({'name': "Client", 'ip_address': "localhost"}),
                                    content_type='application/json')
        assert_successfully_created(response)
        response = self.client.patch('/clients/' + str(client_id),
                                     data=json.dumps({'name': new_name, 'ip_address': 'localhost'}),
                                     content_type='application/json')
        assert_status_code_equal(response, status.HTTP_204_NO_CONTENT)

        client = Client.query.filter_by(id=client_id).first()
        self.assertEqual(client.name, new_name)
