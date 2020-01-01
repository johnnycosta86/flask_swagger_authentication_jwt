from flask import Flask, Blueprint, jsonify
from api.user_resource import user
from api.train_resource import training
from api.predict_resource import predicting
from api.authentication_resource import authentication

from core.utils.restplus import api
from core.utils.log import log
from flask_jwt_extended import JWTManager
from core.utils.blacklist import BLACKLIST

app = Flask(__name__)
jwt = JWTManager(app)

port = 8080
host = '0.0.0.0'

def initialize_app(app):
    app.config['RESTPLUS_VALIDATE'] = True
    app.config['ERROR_404_HELP'] = False
    app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['SERVER_NAME'] = "{}:{}".format(host, port)

    blueprint = Blueprint('api', __name__)
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    api.add_namespace(authentication)
    api.add_namespace(training)
    api.add_namespace(predicting)
    api.add_namespace(user)


@jwt.token_in_blacklist_loader
def verify_blacklist(token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_invalidate():
    return jsonify({'message': 'You have been logged out.'}), 401  # unauthorized


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=True, port=port, host=host)


if __name__ == '__main__':
    main()
