import unittest
from app.db_helper import DbHelper
from app.models.client import Client
from app.models.dataset import Dataset

IP_ADDRESS = '127.0.0.1'
FILENAME='file.txt'


class TestDbHelper(unittest.TestCase):
    def test_client_has_dataset_returns_true(self):
        client = Client(name='Client', ip_address=IP_ADDRESS)
        dataset = Dataset(filename=FILENAME)
        client.datasets = [dataset]

        result = DbHelper.client_has_dataset(client, dataset)
        self.assertTrue(result)

    def test_client_has_dataset_returns_false(self):
        client = Client(name='Client', ip_address=IP_ADDRESS)
        dataset = Dataset(filename=FILENAME)

        result = DbHelper.client_has_dataset(client, dataset)
        self.assertFalse(result)
