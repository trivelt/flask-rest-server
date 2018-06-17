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
        if self._invalid_data(input_data):
            abort(status.HTTP_400_BAD_REQUEST, "Received incorrect data: %s" % str(request.get_data()))

        client_id = input_data['client']
        client = DbHelper.get_client(client_id)
        if not client:
            abort(status.HTTP_400_BAD_REQUEST, "Specified client %s does not exist" % client_id)

        new_dataset = self._create_dataset(input_data)
        if DbHelper.client_has_dataset(client, new_dataset):
            abort(status.HTTP_409_CONFLICT, "Could not overwrite existing dataset. "
                                            "Use PATCH to modify resource or DELETE to remove it")

        return self._add_dataset(client, new_dataset)

    def _invalid_data(self, json_data):
        if json_data is None:
            return True
        return not ('client' in json_data and 'filename' in json_data)

    def _create_dataset(self, json_data):
        dataset = Dataset(filename=json_data['filename'])
        self._insert_metadata(json_data, dataset)
        return dataset

    def _insert_metadata(self, input, dataset):
        metadata_dict = {}
        for key, value in input.items():
            if key not in ['client', 'filename']:
                metadata_dict[key] = value
        dataset.set_userdata(metadata_dict)

    def _add_dataset(self, client, dataset):
        if not client.datasets:
            client.datasets = [dataset]
        else:
            client.datasets.append(dataset)
        db.session.commit()

        return '', status.HTTP_201_CREATED
