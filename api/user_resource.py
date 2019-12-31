from flask_restplus import reqparse
from core.utils.restplus import api
from flask_restplus import Resource
from core.model.user_model import UserModel
import traceback
from flask_jwt_extended import jwt_required

user = api.namespace('users', description='Manage users')

users = {}

attributes = reqparse.RequestParser()
attributes.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")
attributes.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank.")
attributes.add_argument('email', type=str, required=True, help="The field 'email' cannot be left blank.")
attributes.add_argument('active', type=bool, required=True, help="The field 'active' cannot be left blank.")


@user.route("/<int:user_id>")
class UserList(Resource):
    @jwt_required
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'user_id': 'Specify the Id associated with the user'})
    def get(self, user_id):
        user_found = UserModel.find_user(user_id)
        if user_found:
            return user_found.json()
        return {'message': 'User not found.'}, 404

    @jwt_required
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'user_id': 'Specify the Id associated with the user'})
    def delete(self, user_id):
        user_found = UserModel.find_user(user_id)
        if user_found:
            user_deleted = user_found.delete_user()
            return {'message': 'User deleted: {}'.format(user_deleted.json())}, 200
        return {'message': 'User not found.'}, 404


@user.route("/")
class UserResource(Resource):
    @jwt_required
    @api.doc(responses={200: 'OK', 404: 'Not Found', 500: 'Mapping Key Error'})
    def get(self):
        users_found = UserModel.find_all()
        if users_found:
            return [user_found.json() for user_found in users_found]
        return {}, 200

    @jwt_required
    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'login': 'Specify the login associated with the user',
                     'password': 'Specify the password associated with the user',
                     'email': 'Specify the email associated with the user',
                     'active': 'Specify the active associated with the user'})
    @api.expect(attributes)
    def post(self):
        data = attributes.parse_args()
        if not data.get('login') or data.get('login') is None:
            return {"message": "The field 'login' cannot be left blank."}, 400

        if not data.get('password') or data.get('password') is None:
            return {"message": "The field 'password' cannot be left blank."}, 400

        if not data.get('email') or data.get('email') is None:
            return {"message": "The field 'email' cannot be left blank."}, 400

        print(data.get('active'))

        if data.get('active') is None:
            return {"message": "The field 'active' cannot be left blank."}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": "The email '{}' already exists.".format(data['email'])}, 400

        if UserModel.find_by_login(data['login']):
            return {"message": "The login '{}' already exists.".format(data['login'])}, 400  # Bad Request

        user_new = UserModel(**data)

        try:
            user_new.save_user()
        except:
            user.delete_user()
            traceback.print_exc()
            return {'message': 'An internal server error has ocurred.'}, 500
        return {'message': 'User created successfully!'}, 201  # Created
