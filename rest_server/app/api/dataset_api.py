from app import db
from app.models.dataset import Dataset
from app.db_helper import DbHelper
from flask_restful import Resource
from flask_api import status
from flask import jsonify, abort, request

class DatasetApi(Resource):
    def get(self, id):
        try:
            dataset = Dataset.query.filter_by(id=id).one()
            return jsonify(dataset.json())
        except:
            abort(status.HTTP_404_NOT_FOUND)

    def patch(self, id):
        if not DbHelper.dataset_id_exists(id):
            abort(status.HTTP_404_NOT_FOUND)

        json_data = request.get_json()
        dataset = DbHelper.get_dataset(id)

        if 'client' in json_data:
            client_id = json_data['client']
            if not DbHelper.client_id_exists(client_id):
                abort(status.HTTP_400_BAD_REQUEST)
            dataset.client_id = client_id
        if 'filename' in json_data:
            dataset.filename = json_data['filename']
        db.session.commit()

        return '', status.HTTP_204_NO_CONTENT

    def delete(self, id):
        if not DbHelper.dataset_id_exists(id):
            abort(status.HTTP_404_NOT_FOUND)

        Dataset.query.filter_by(id=id).delete()
        db.session.commit()
        return '', status.HTTP_204_NO_CONTENT
