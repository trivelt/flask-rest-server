from app import db


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    client = db.relationship("Client", back_populates="datasets")
    filename = db.Column(db.String(255))
    userdata = db.Column(db.Text)

    def __repr__(self):
        return "<Dataset(client=%s, filename=%s>" % (str(self.client), self.filename)

    def json(self):
        return {"id": self.id,
                "client_id": self.client_id,
                "filename": self.filename}
