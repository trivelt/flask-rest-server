import unittest
from flask_api import status
from app import create_test_app, db
from app.models.dataset import Dataset
from app.models.client import Client
from start_rest import prepare_app
from tests.tests_utils import *
import json


class TestDatasetsListApi(unittest.TestCase):
    def setUp(self):
        self.app, api = create_test_app()
        self.client = self.app.test_client()
        prepare_app(api)

    def tearDown(self):
        db.session.rollback()
        db.drop_all()
        self.app.app_context().push()

    def test_get_datasets_empty_list(self):
        response = self.client.get('/datasets')
        assert_success(response)
        self.assertEqual(response.get_json(), [])

    def test_get_nonempty_datasets_list(self):
        client = Client(name='Client', ip_address='127.0.0.1')
        first_dataset = Dataset(filename='test.mp3')
        second_dataset = Dataset(filename='movie.mp4')
        client.datasets = [first_dataset, second_dataset]
        db.session.add(client)
        db.session.commit()

        response = self.client.get('/datasets')
        response_json = response.get_json()

        assert_success(response)
        self.assertEqual(len(response_json), 2)
        self.assertDictEqual(response_json[0], first_dataset.json())
        self.assertDictEqual(response_json[1], second_dataset.json())

    def test_add_dataset(self):
        client = Client(name='Client', ip_address='127.0.0.1')
        db.session.add(client)
        db.session.commit()

        filename = 'foo.bar'
        response = self.client.post('/datasets', data=json.dumps({'client': client.id, 'filename': filename}),
                                    content_type='application/json')
        assert_successfully_created(response)

        self.assertEqual(Dataset.query.count(), 1)
        dataset = Dataset.query.first()
        self.assertEqual(dataset.client_id, client.id)
        self.assertEqual(dataset.client, client)
        self.assertEqual(dataset.filename, filename)

    def test_add_two_datasets_for_same_client_successfully(self):
        filename1 = 'foo.txt'
        filename2 = 'bar.txt'
        client = Client(name='Client', ip_address='127.0.0.1')
        db.session.add(client)
        db.session.commit()

        response = self.client.post('/datasets', data=json.dumps({'client': client.id, 'filename': filename1}),
                                    content_type='application/json')
        assert_successfully_created(response)
        response = self.client.post('/datasets', data=json.dumps({'client': client.id, 'filename': filename2}),
                                    content_type='application/json')
        assert_successfully_created(response)

        self.assertEqual(len(client.datasets), 2)
        self.assertEqual(client.datasets[0].filename, filename1)
        self.assertEqual(client.datasets[1].filename, filename2)

    def test_dataset_not_created_because_of_missing_mandatory_parameter(self):
        response = self.client.post('/datasets', data=json.dumps({'filename': 'file.txt'}),
                                    content_type='application/json')
        assert_status_code_equal(response, status.HTTP_400_BAD_REQUEST)

    def test_dataset_not_created_because_specified_client_not_exists(self):
        response = self.client.post('/datasets', data=json.dumps({'client': 1, 'filename': 'file.txt'}),
                                    content_type='application/json')
        assert_status_code_equal(response, status.HTTP_400_BAD_REQUEST)

    def test_dataset_not_created_because_already_exists(self):
        filename = 'test.txt'
        client = Client(name='Client', ip_address='127.0.0.1')
        db.session.add(client)
        client.datasets = [Dataset(filename=filename)]
        db.session.commit()

        response = self.client.post('/datasets', data=json.dumps({'client': client.id, 'filename': filename}),
                                    content_type='application/json')

        assert_status_code_equal(response, status.HTTP_409_CONFLICT)

    def test_create_dataset_with_userdefined_metadata(self):
        key = 'someKey'
        value = 'someValue'
        second_key ='key2'
        second_value = 'val'
        client = Client(name='Client', ip_address='127.0.0.1')
        db.session.add(client)
        db.session.commit()

        response = self.client.post('/datasets',
                                    data=json.dumps({'client': client.id, 'filename': 'foo.txt',
                                                     key: value, second_key: second_value}),
                                    content_type='application/json')

        assert_successfully_created(response)
        dataset = Dataset.query.first()
        assert_unordered_list_equal(dataset.get_keys(), [key, second_key])
        self.assertEqual(dataset.get_value(key), value)
        self.assertEqual(dataset.get_value(second_key), second_value)
