from app import db
from app.models.dataset import Dataset

MAX_NAME_LENGTH = 255
MAX_IP_LENGTH = 45


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_NAME_LENGTH))
    ip_address = db.Column(db.String(MAX_IP_LENGTH))
    datasets = db.relationship('Dataset', order_by=Dataset.id, back_populates='client')

    def __repr__(self):
        return "<Client(name=%s, ip=%s>" % (self.name, self.ip_address)

    def json(self):
        return {'id': self.id,
                'name': self.name,
                'ip_address': self.ip_address}

    def details_json(self):
        details = self.json()
        details.update({'datasets': [dataset.id for dataset in self.datasets]})
        return details
