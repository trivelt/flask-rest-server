from app.api.client_api import ClientApi
from app.api.clients_list_api import ClientsListApi
from app.api.datasets_list_api import DatasetsListApi
from app.api.dataset_api import DatasetApi


def configure_routes(api):
    api.add_resource(ClientsListApi, '/clients')
    api.add_resource(ClientApi, '/clients/<id>')
    api.add_resource(DatasetsListApi, '/datasets')
    api.add_resource(DatasetApi, '/datasets/<id>')
