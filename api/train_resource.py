from core.utils.restplus import api
from flask import request
from flask_restplus import Resource, fields

training = api.namespace('Training', description='Training Machine Learning Models')

list_of_tasks = {}

model = api.model('Training Models',
                  {'train': fields.String(required=True,
                                         description="Training Value",
                                         help="Train cannot be blank.")})

@training.route("/<int:id>")
class TrainingResource(Resource):

    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'id': 'Specify the Id associated with the train'})
    def get(self, id):
        try:
            name = list_of_tasks[id]
            return {
                "status": "Task retrieved",
                "name": list_of_tasks[id]
            }
        except KeyError as e:
            training.abort(404, e.__doc__, status="Could not retrieve information", statusCode="404")

    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'id': 'Specify the Id associated with the train'})
    @api.expect(model)
    def post(self, id):
        try:
            list_of_tasks[id] = request.json['train']
            return {
                "status": "New task added",
                "name": list_of_tasks[id]
            }
        except KeyError as e:
            training.abort(500, e.__doc__, status="Could not save information", statusCode="500")
        except Exception as e:
            training.abort(400, e.__doc__, status="Could not save information", statusCode="400")