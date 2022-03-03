from flask import Response, request
from database.models import Brevet
from flask_restful import Resource
import dateutil.parser


class BrevetAPI(Resource):
    def get(self, id):
        brevet = Brevet.objects.get(id=id).to_json()
        return Response(brevet, mimetype="application/json", status=200)

    def put(self, id):
        body = request.get_json()
        Brevet.objects.get(id=id).update(**body)
        return {'id': str(id), 'status': 'updated'}, 200

    def delete(self, id):
        Brevet.objects.get(id=id).delete()
        return {'id': str(id), 'status': 'deleted'}, 200