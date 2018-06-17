from app import db
from app.db_helper import DbHelper
import app.api.swagger_docs as docs
from flask_restful_swagger import swagger
from flask_restful import Resource
from flask_api import status
from flask import jsonify, abort, request


class DatasetApi(Resource):
    @swagger.operation(
        summary='Returns details of specific dataset',
        parameters=[docs.DatasetIdParam],
        responseMessages=[docs.Error_CouldNotFindResource]
    )
    def get(self, id):
        dataset = DbHelper.get_dataset(id)
        if not dataset:
            abort(status.HTTP_404_NOT_FOUND, "Could not find dataset %s" % id)
        return jsonify(dataset.details_json())

    @swagger.operation(
        summary='Modifies dataset',
        parameters=[docs.DatasetIdParam, docs.DatasetOptionalBodyParam],
        responseMessages=[docs.Error_CouldNotFindResource,
                          docs.Error_BadRequest("Could not find specified client")]
    )
    def patch(self, id):
        dataset = DbHelper.get_dataset(id)
        if not dataset:
            abort(status.HTTP_404_NOT_FOUND, "Could not patch non existent dataset")

        self._update_dataset(dataset)
        return '', status.HTTP_204_NO_CONTENT

    @swagger.operation(
        summary='Deletes dataset',
        parameters=[docs.DatasetIdParam],
        responseMessages=[docs.Error_CouldNotFindResource]
    )
    def delete(self, id):
        if not DbHelper.dataset_id_exists(id):
            abort(status.HTTP_404_NOT_FOUND, "Could not delete non existent dataset")

        DbHelper.delete_dataset(id)
        return '', status.HTTP_204_NO_CONTENT

    def _update_dataset(self, dataset):
        json_data = request.get_json()
        if 'client' in json_data:
            client_id = json_data['client']
            if not DbHelper.client_id_exists(client_id):
                abort(status.HTTP_400_BAD_REQUEST, "Specified client %s does not exist" % client_id)
            dataset.client_id = client_id
        if 'filename' in json_data:
            dataset.filename = json_data['filename']
        self._update_metadata(json_data, dataset)
        db.session.commit()

    def _update_metadata(self, input, dataset):
        metadata_dict = {}
        for key, value in input.items():
            if key not in ['client', 'filename']:
                metadata_dict[key] = value
        if dataset.userdata:
            userdata_dict = dataset.get_userdata()
            userdata_dict.update(metadata_dict)
            metadata_dict = userdata_dict
        dataset.set_userdata(metadata_dict)
