from app import db
from app.models.client import Client
from app.db_helper import DbHelper
from flask_restful import Resource
from flask_api import status
from flask import jsonify, abort, request


class ClientApi(Resource):
    def get(self, id):
        try:
            client = Client.query.filter(Client.id == id).one()
            return jsonify(client.json())
        except:
            abort(status.HTTP_404_NOT_FOUND)

    def patch(self, id):
        if not DbHelper.client_id_exists(id):
            return abort(status.HTTP_400_BAD_REQUEST)

        json_data = request.get_json()
        client = DbHelper.get_client(id)
        client.name = json_data['name']
        client.ip_address = json_data['ip_address']
        db.session.commit()
        return '', status.HTTP_204_NO_CONTENT

    def delete(self, id):
        return '', status.HTTP_204_NO_CONTENT
        # TODO: delete client
