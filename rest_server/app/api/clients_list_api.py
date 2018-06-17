from app import db
from app.models.client import Client
from app.db_helper import DbHelper
from flask_restful import Resource
from flask_api import status
from flask import request, jsonify, abort


class ClientsListApi(Resource):
    def get(self):
        clients = [client.json() for client in Client.query.all()]
        return jsonify(clients)

    def post(self):
        input_data = request.get_json()
        if self._invalid_data(input_data):
            abort(status.HTTP_400_BAD_REQUEST, "Received incorrect data: %s" % str(request.get_data()))

        new_client = Client(name=input_data['name'], ip_address=input_data['ip_address'])
        if DbHelper.client_exists(new_client):
            abort(status.HTTP_409_CONFLICT, "Could not overwrite existing client. "
                                            "Use PATCH to modify resource or DELETE to remove it")

        return self._add_client(new_client)

    def _invalid_data(self, json_data):
        if json_data is None:
            return True
        return not ('name' in json_data and 'ip_address' in json_data)

    def _add_client(self, client):
        db.session.add(client)
        db.session.commit()
        return '', status.HTTP_201_CREATED
