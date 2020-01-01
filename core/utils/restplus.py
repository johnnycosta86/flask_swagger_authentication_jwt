from core.utils.log import log
from flask_restplus import Api

authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
    }
}

api = Api(version='1.0', title='Crypto API',
          description='This Page allows you to explore and interact with Robot Crypto REST API. '
                      'Click the sections below to see details of the resources and how to use them \n'
                      'By default, The REST API is only available via HTTPS. \n\n'
                      'Before you can try any of the operations, you must click Authentication and enter suitable '
                      'credentials',
          security='apiKey', authorizations=authorizations)

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    return {'message': message}, 500
