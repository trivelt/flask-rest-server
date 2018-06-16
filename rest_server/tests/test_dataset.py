import unittest
from app.models.client import Client
from app.models.dataset import Dataset


class TestClient(unittest.TestCase):
    def setUp(self):
        self.id = 3
        self.client_id = 2
        self.filename = 'test.txt'

    def test_json(self):
        dataset= Dataset(filename=self.filename, id=self.id, client_id=self.client_id)
        self.assertDictEqual(dataset.json(), {'id': self.id,
                                              'client': self.client_id,
                                              'filename': self.filename})

    def test_details_json(self):
        dataset= Dataset(filename=self.filename, id=self.id, client_id=self.client_id)
        dataset.set_userdata({'key': 'value',
                              'key2': 'value2'})
        self.assertDictEqual(dataset.details_json(), {'id': self.id,
                                                      'client': self.client_id,
                                                      'filename': self.filename,
                                                      'key2': 'value2',
                                                      'key': 'value'})
