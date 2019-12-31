from core.utils.restplus import api
from flask import request
from flask_restplus import Resource, fields

predicting = api.namespace('Predicting', description='Predicting Future Using Machine Learning Models')

list_of_tasks = {}

model = api.model('Training Model',
                  {'task': fields.String(required=True,
                                         description="Task Value",
                                         help="Task cannot be blank.")})

@predicting.route("/<int:id>")
class PredictingResource(Resource):

    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'id': 'Specify the Id associated with the task'})
    def get(self, id):
        try:
            name = list_of_tasks[id]
            return {
                "status": "Task retrieved",
                "name": list_of_tasks[id]
            }
        except KeyError as e:
            predicting.abort(404, e.__doc__, status="Could not retrieve information", statusCode="404")

    @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'id': 'Specify the Id associated with the task'})
    @api.expect(model)
    def post(self, id):
        try:
            list_of_tasks[id] = request.json['task']
            return {
                "status": "New task added",
                "name": list_of_tasks[id]
            }
        except KeyError as e:
            predicting.abort(500, e.__doc__, status="Could not save information", statusCode="500")
        except Exception as e:
            predicting.abort(400, e.__doc__, status="Could not save information", statusCode="400")