from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, get_raw_jwt, jwt_required
from core.model.user_model import UserModel
from core.utils.blacklist import BLACKLIST
from core.utils.restplus import api
from flask_restplus import Resource, reqparse, fields

authentication = api.namespace('authentication', description='Manage authentication session')

list_of_tasks = {}

attributes = reqparse.RequestParser()
attributes.add_argument('login', type=str, default='admin', required=True,  help="The field 'login' cannot be left blank.")
attributes.add_argument('password', type=str, default='admin', required=True, help="The field 'password' cannot be left blank.")

model = {
    'login': fields.String(default='admin'),
    'password': fields.String(default='admin')
}


@authentication.route("/login")
class AuthenticationLogin(Resource):

    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'login': 'Specify the login associated with the user',
                     'password': 'Specify the password associated with the user'})
    @api.expect(attributes)
    def post(self):
        data = attributes.parse_args()
        if not data.get('login') or data.get('login') is None:
            return {"message": "The field 'login' cannot be left blank."}, 400

        if not data.get('password') or data.get('password') is None:
            return {"message": "The field 'password' cannot be left blank."}, 400

        user_found = UserModel.find_by_login(data['login'])

        if user_found and safe_str_cmp(user_found.password, data['password']):
            if user_found.active:
                token = create_access_token(identity=user_found.user_id)
                return {'access_token': 'Bearer {}'.format(token)}, 200
            return {'message': 'User not confirmed.'}, 400
        return {'message': 'The username or password is incorrect.'}, 401  # Unauthorized


@authentication.route("/logoff")
class AuthenticationLogoff(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']  # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200
