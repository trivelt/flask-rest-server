from app.models.client import Client

class DbHelper(object):

    @staticmethod
    def client_exists(client):
        return Client.query.filter_by(name=client.name).filter_by(ip_address=client.ip_address).count() > 0
