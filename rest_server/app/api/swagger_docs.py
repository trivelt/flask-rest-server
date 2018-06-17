from flask_restful_swagger import swagger


@swagger.model
class ClientModel(object):
    def __init__(self, name, ip_address):
        pass


@swagger.model
class ClientModelOpt(object):
    def __init__(self, name='', ip_address=''):
        pass


@swagger.model
class DatasetModel(object):
    def __init__(self, client, filename, some_key='someValue', **kwargs):
        pass


@swagger.model
class DatasetModelOpt(object):
    def __init__(self, client='', filename='', some_key='someValue', **kwargs):
        pass

ClientIdParam = {'name': 'id',
                 'description': 'Client ID',
                 'required': True,
                 'dataType': 'integer',
                 'paramType': 'path'
}

ClientFullBodyParam = {'name': 'body',
                       'description': 'Client object',
                       'required': True,
                       'allowMultiple': False,
                       'dataType': ClientModel.__name__,
                       'paramType': 'body'
}

ClientOptionalBodyParam = {"name": "body",
                           "description": "Client object",
                           "required": True,
                           "allowMultiple": False,
                           "dataType": ClientModelOpt.__name__,
                           "paramType": "body"
}

DatasetIdParam = {'name': 'id',
                  'description': 'Dataset ID',
                  'required': True,
                  'dataType': 'integer',
                  'paramType': 'path'
}

DatasetFullBodyParam = {'name': 'body',
                        'description': 'Dataset object',
                        'required': True,
                        'allowMultiple': False,
                        'dataType': DatasetModel.__name__,
                        'paramType': 'body'
}

DatasetOptionalBodyParam = {"name": "body",
                            "description": "Dataset object",
                            "required": True,
                            "allowMultiple": False,
                            "dataType": DatasetModelOpt.__name__,
                            "paramType": "body"
}

Error_CouldNotFindResource = {'code': 404,
                            'message': 'Could not find requested resource'
                            }

Error_BadRequest = lambda msg : {'code': 404,
                                 'message': msg
                                 }

Error_ResourceAlreadyExists = {'code': 409,
                  'message': 'Resource already exists'
                  }
