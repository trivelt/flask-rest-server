import unittest
from flask_api import status
from app import create_test_app, db
from app.models.dataset import Dataset
from app.models.client import Client
from start_rest import prepare_app
from tests.tests_utils import *
import json


class TestDatasetApi(unittest.TestCase):
    def setUp(self):
        self.app, api = create_test_app()
        self.client = self.app.test_client()
        prepare_app(api)

    def tearDown(self):
        db.drop_all()
        self.app.app_context().push()

    def test_cannot_get_nonexistent_dataset(self):
        response = self.client.get('/datasets/1')
        assert_status_code_equal(response, status.HTTP_404_NOT_FOUND)

    def test_get_dataset_successfully(self):
        dataset = Dataset(client_id=1, filename='foo.txt')
        dataset.set_userdata({'key': 'value'})
        db.session.add(dataset)
        db.session.commit()

        response = self.client.get('/datasets/1')
        assert_success(response)
        self.assertEqual(response.get_json(), dataset.details_json())

    def test_cannot_patch_nonexistent_dataset(self):
        response = self.client.patch('/datasets/1', data=json.dumps({'client': 1, 'filename': 'foo.txt'}),
                                     content_type='application/json')
        assert_status_code_equal(response, status.HTTP_404_NOT_FOUND)

    def test_patch_dataset_successfully(self):
        new_filename = 'bar.txt'
        dataset = Dataset(client_id=1, filename='foo.txt')
        db.session.add(dataset)
        db.session.commit()

        response = self.client.patch('/datasets/' + str(dataset.id),
                                     data=json.dumps({'filename': new_filename}),
                                     content_type='application/json')

        assert_status_code_equal(response, status.HTTP_204_NO_CONTENT)
        self.assertEqual(dataset.filename, new_filename)

    def test_patch_adding_userdefined_metadata(self):
        key = 'some_key'
        value = 'some_value'
        dataset = Dataset(client_id=1, filename='foo.txt')
        db.session.add(dataset)
        db.session.commit()

        response = self.client.patch('/datasets/' + str(dataset.id),
                                     data=json.dumps({key: value}),
                                     content_type='application/json')

        assert_status_code_equal(response, status.HTTP_204_NO_CONTENT)
        self.assertEqual(dataset.get_value(key), value)

    def test_patch_overwriting_userdefined_metadata(self):
        key = 'some_key'
        value = 'some_value'
        new_value = 'new value'
        dataset = Dataset(client_id=1, filename='foo.txt')
        dataset.set_userdata({key: value})
        db.session.add(dataset)
        db.session.commit()

        response = self.client.patch('/datasets/' + str(dataset.id),
                                     data=json.dumps({key: new_value}),
                                     content_type='application/json')

        assert_status_code_equal(response, status.HTTP_204_NO_CONTENT)
        self.assertEqual(dataset.get_value(key), new_value)

    def test_patch_changing_owner_of_dataset(self):
        client1 = Client(name='Client1', ip_address='127.0.0.1')
        client2 = Client(name='Client2', ip_address='127.0.0.2')
        dataset = Dataset(filename='test.txt')
        client1.datasets = [dataset]
        db.session.add_all([client1, client2])
        db.session.commit()

        response = self.client.patch('/datasets/' + str(dataset.id),
                                     data=json.dumps({'client': client2.id}),
                                     content_type='application/json')

        assert_status_code_equal(response, status.HTTP_204_NO_CONTENT)
        self.assertEqual(client1.datasets, [])
        self.assertEqual(client2.datasets, [dataset])
        self.assertEqual(dataset.client, client2)

    def test_cannot_patch_changing_owner_because_not_exists(self):
        client = Client(name='Client1', ip_address='127.0.0.1')
        dataset = Dataset(filename='test.txt')
        client.datasets = [dataset]
        db.session.add(client)
        db.session.commit()

        response = self.client.patch('/datasets/' + str(dataset.id),
                                     data=json.dumps({'client': 42}),
                                     content_type='application/json')

        assert_status_code_equal(response, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(client.datasets, [dataset])

    def test_cannot_delete_nonexistent_dataset(self):
        response = self.client.delete('/datasets/1')
        assert_status_code_equal(response, status.HTTP_404_NOT_FOUND)

    def test_delete_dataset_successfully(self):
        db.session.add(Dataset(client_id=1, filename='foo.txt'))
        db.session.commit()

        response = self.client.delete('/datasets/1')

        assert_status_code_equal(response, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dataset.query.all(), [])
