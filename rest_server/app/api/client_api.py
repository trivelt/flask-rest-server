from app import db
from app.models.client import Client
from flask_restful import Resource
from flask_api import status
from flask import jsonify, abort


class ClientApi(Resource):
    def get(self, id):
        try:
            client = Client.query.filter(Client.id == id).one()
            return jsonify(client.json())
        except:
            abort(status.HTTP_404_NOT_FOUND)

    def patch(self, id):
        return '', status.HTTP_204_NO_CONTENT
        # TODO: update client

    def delete(self, id):
        return '', status.HTTP_204_NO_CONTENT
        # TODO: delete client
