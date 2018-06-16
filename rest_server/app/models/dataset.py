from app import db
import json


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    client = db.relationship("Client", back_populates="datasets")
    filename = db.Column(db.String(255))
    userdata = db.Column(db.Text)

    def __repr__(self):
        return "<Dataset(client=%s, filename=%s>" % (str(self.client), self.filename)

    def get_keys(self):
        try:
            return list(json.loads(self.userdata).keys())
        except:
            return []

    def get_value(self, key):
        try:
            return json.loads(self.userdata)[key]
        except:
            return None

    def get_userdata(self):
        return json.loads(self.userdata)

    def set_userdata(self, data):
        self.userdata = json.dumps(data)

    def json(self):
        return {"id": self.id,
                "client_id": self.client_id,
                "filename": self.filename}
