from app.models.client import Client
from app.models.dataset import Dataset


class DbHelper(object):

    @staticmethod
    def client_exists(client):
        return Client.query.filter_by(name=client.name).filter_by(ip_address=client.ip_address).count() > 0

    @staticmethod
    def client_id_exists(id):
        return Client.query.filter_by(id=id).count() > 0

    @staticmethod
    def get_client(id):
        return Client.query.filter_by(id=id).one()

    @staticmethod
    def client_has_dataset(client, dataset):
        for client_dataset in client.datasets:
            if client_dataset.filename == dataset.filename:
                return True
        return False

    @staticmethod
    def dataset_id_exists(id):
        return Dataset.query.filter_by(id=id).count() > 0

    @staticmethod
    def get_dataset(id):
        return Dataset.query.filter_by(id=id).one()
