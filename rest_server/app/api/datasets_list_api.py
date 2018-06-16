from app import db
from app.models.dataset import Dataset
from app.db_helper import DbHelper
from flask_restful import Resource
from flask_api import status
from flask import request, jsonify, abort


class DatasetsListApi(Resource):
    def get(self):
        datasets = [dataset.json() for dataset in Dataset.query.all()]
        return jsonify(datasets)

    def post(self):
        input_data = request.get_json()
        if self._invalid_data():
            # print('Received incorrect data: ' + str(request.get_data()))
            abort(status.HTTP_400_BAD_REQUEST)

        client_id = input_data['client']
        if not DbHelper.client_id_exists(client_id):
            abort(status.HTTP_404_NOT_FOUND)

        new_dataset = Dataset(filename=input_data['filename'])
        client = DbHelper.get_client(client_id)

        if DbHelper.client_has_dataset(client, new_dataset):
            abort(status.HTTP_409_CONFLICT)

        if not client.datasets:
            client.datasets = [new_dataset]
        else:
            client.datasets.append(new_dataset)
        db.session.commit()

        return '', status.HTTP_201_CREATED


    def _invalid_data(self):
        json_data = request.get_json()
        if json_data is None:
            return True
        return not ('client' in json_data and 'filename' in json_data)
