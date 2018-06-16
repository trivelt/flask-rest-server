import unittest
from app.models.client import Client
from app.models.dataset import Dataset


class TestClient(unittest.TestCase):
    def setUp(self):
        self.id = 2
        self.name = 'Client'
        self.ip_address = '127.0.0.1'

    def test_json(self):
        client = Client(name=self.name, ip_address=self.ip_address, id=self.id)
        self.assertDictEqual(client.json(), {'name': self.name,
                                             'ip_address': self.ip_address,
                                             'id': self.id})

    def test_details_json(self):
        client = Client(name=self.name, ip_address=self.ip_address, id=self.id)
        client.datasets = [Dataset(filename='foo.bar', id=1),
                           Dataset(filename='test', id=3)]
        self.assertDictEqual(client.details_json(), {'name': self.name,
                                                     'ip_address': self.ip_address,
                                                     'id': self.id,
                                                     'datasets': [1, 3]})
