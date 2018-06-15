from app.api.client_api import ClientApi
from app.api.clients_list_api import ClientsListApi


def configure_routes(api):
    api.add_resource(ClientsListApi, '/clients')
    api.add_resource(ClientApi, '/clients/<id>')
