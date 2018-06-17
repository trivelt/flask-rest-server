from app import db
from app.models.client import Client
from app.db_helper import DbHelper
from app.data_validator import DataValidator
import app.api.swagger_docs as docs
from flask_restful_swagger import swagger
from flask_restful import Resource
from flask_api import status
from flask import request, jsonify, abort


class ClientsListApi(Resource):
    @swagger.operation(summary='Returns list of clients')
    def get(self):
        clients = [client.json() for client in Client.query.all()]
        return jsonify(clients)

    @swagger.operation(
        summary='Creates new client',
        parameters=[docs.ClientFullBodyParam],
        responseMessages=[docs.Error_ResourceAlreadyExists,
                          docs.Error_BadRequest("Invalid data")]
    )
    def post(self):
        input_data = request.get_json()
        self._validate_data(input_data)

        new_client = Client(name=input_data['name'], ip_address=input_data['ip_address'])
        if DbHelper.client_exists(new_client):
            abort(status.HTTP_409_CONFLICT, "Could not overwrite existing client. "
                                            "Use PATCH to modify resource or DELETE to remove it")

        return self._add_client(new_client)

    def _validate_data(self, json_data):
        if json_data is None:
            abort(status.HTTP_400_BAD_REQUEST, "Incorrect JSON data: %s" % str(request.get_data()))

        if not ('name' in json_data and 'ip_address' in json_data):
            abort(status.HTTP_400_BAD_REQUEST, "Request does not contain all mandatory fields [name, ip_address]")

        ip_address = json_data['ip_address']
        if DataValidator.is_invalid_ip(ip_address):
            abort(status.HTTP_400_BAD_REQUEST, "Invalid IP address %s" % ip_address)

    def _add_client(self, client):
        db.session.add(client)
        db.session.commit()
        return '', status.HTTP_201_CREATED
