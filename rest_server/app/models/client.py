from app import db
from app.models.dataset import Dataset


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    ip_address = db.Column(db.String(80))
    datasets = db.relationship("Dataset", order_by=Dataset.id, back_populates="client")

    def __repr__(self):
        return "<Client(name=%s, ip=%s>" % (self.name, self.ip_address)
