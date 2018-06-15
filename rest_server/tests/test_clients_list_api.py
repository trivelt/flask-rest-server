import unittest
from flask_api import status
from app import create_test_app, db
from app.models.client import Client
from start_rest import prepare_app
from tests.tests_utils import *
import json
import mock


class TestClientsListApi(unittest.TestCase):
    def setUp(self):
        self.app, api = create_test_app()
        self.client = self.app.test_client()
        prepare_app(api)

    def tearDown(self):
        db.drop_all()
        self.app.app_context().push()

    def test_get_clients_empty_list(self):
        response = self.client.get('/clients')
        assert_success(response)
        self.assertEqual(response.get_json(), [])

    def test_get_one_element_clients_list(self):
        client = Client(name="Foo", ip_address="localhost")
        db.session.add(client)
        db.session.commit()

        response = self.client.get('/clients')
        response_json = response.get_json()
        assert_success(response)
        self.assertEqual(len(response_json), 1)
        self.assertDictEqual(response_json[0], client.json())

    def test_get_multiple_clients(self):
        db.session.add_all([Client(name="Foo", ip_address="localhost"),
                            Client(name="Bar", ip_address="127.0.0.1")])
        db.session.commit()

        response = self.client.get('/clients')
        response_json = response.get_json()
        assert_success(response)
        self.assertEqual(len(response_json), 2)

    def test_create_client_successfully(self):
        name = "Client1"
        ip_address = "10.11.0.5"
        self.assertEqual(len(Client.query.filter(Client.name == name, Client.ip_address == ip_address).all()), 0)

        response = self.client.post('/clients', data=json.dumps({'name': name, 'ip_address': ip_address}),
                                    content_type='application/json')

        assert_successfully_created(response)
        self.assertEqual(len(Client.query.filter(Client.name == name, Client.ip_address == ip_address).all()), 1)

    def test_client_not_created_because_of_wrong_input_data(self):
        response = self.client.post('/clients', data=json.dumps({'name': "Foo"}),
                                    content_type='application/json')
        assert_status_code_equal(response, status.HTTP_400_BAD_REQUEST)

    def test_client_already_exists(self):
        self.client.post('/clients', data=json.dumps({'name': "Client", 'ip_address': "localhost"}),
                         content_type='application/json')
        response = self.client.post('/clients', data=json.dumps({'name': "Client", 'ip_address': "localhost"}),
                                    content_type='application/json')
        self.assertEqual(len(Client.query.all()), 1)
        assert_status_code_equal(response, status.HTTP_409_CONFLICT)


    @mock.patch('app.db.session.add')
    def test_internal_server_error_during_add_client(self, dbMock):
        dbMock.side_effect = Exception()
        response = self.client.post('/clients', data=json.dumps({'name': 10, 'ip_address': 20}),
                                    content_type='application/json')
        assert_status_code_equal(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
