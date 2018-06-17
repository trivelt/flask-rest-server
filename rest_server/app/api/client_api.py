from app import db
from app.db_helper import DbHelper
from app.data_validator import DataValidator
from flask_restful import Resource
from flask_api import status
from flask import jsonify, abort, request


class ClientApi(Resource):
    def get(self, id):
        client = DbHelper.get_client(id)
        if not client:
            abort(status.HTTP_404_NOT_FOUND, "Could not find client %s" % id)
        return jsonify(client.details_json())

    def patch(self, id):
        client = DbHelper.get_client(id)
        if not client:
            return abort(status.HTTP_404_NOT_FOUND, "Could not patch non existent client")

        self._update_client(client)
        return '', status.HTTP_204_NO_CONTENT

    def delete(self, id):
        if not DbHelper.client_id_exists(id):
            abort(status.HTTP_404_NOT_FOUND, "Could not delete non existent client")

        DbHelper.delete_client(id)
        return '', status.HTTP_204_NO_CONTENT

    def _update_client(self, client):
        json_data = request.get_json()
        if 'name' in json_data:
            client.name = json_data['name']
        if 'ip_address' in json_data:
            ip_address = json_data['ip_address']
            if DataValidator.is_invalid_ip(ip_address):
                abort(status.HTTP_400_BAD_REQUEST, "Invalid IP address %s" % str(ip_address))
            client.ip_address = ip_address
        db.session.commit()
