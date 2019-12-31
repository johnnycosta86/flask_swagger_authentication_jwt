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
          description='Api Crypto using Flask RestPlus', security='apiKey', authorizations=authorizations)

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    return {'message': message}, 500
