from app.models.client import Client
from app.models.dataset import Dataset
from app import db


class DbHelper(object):

    @staticmethod
    def client_exists(client):
        return Client.query.filter_by(name=client.name).filter_by(ip_address=client.ip_address).count() > 0

    @staticmethod
    def client_id_exists(id):
        return DbHelper._object_id_exists(Client, id)

    @staticmethod
    def dataset_id_exists(id):
        return DbHelper._object_id_exists(Dataset, id)

    @staticmethod
    def get_client(id):
        return DbHelper._get_object(Client, id)

    @staticmethod
    def get_dataset(id):
        return DbHelper._get_object(Dataset, id)

    @staticmethod
    def delete_client(id):
        DbHelper._delete_object(Client, id)

    @staticmethod
    def delete_dataset(id):
        DbHelper._delete_object(Dataset, id)

    @staticmethod
    def client_has_dataset(client, dataset):
        for client_dataset in client.datasets:
            if client_dataset.filename == dataset.filename:
                return True
        return False

    @staticmethod
    def _get_object(Class, id):
        try:
            return Class.query.filter_by(id=id).one()
        except:
            return None

    @staticmethod
    def _delete_object(Class, id):
        Class.query.filter_by(id=id).delete()
        db.session.commit()

    @staticmethod
    def _object_id_exists(Class, id):
        return Class.query.filter_by(id=id).count() > 0
