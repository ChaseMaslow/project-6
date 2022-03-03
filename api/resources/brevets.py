from flask import Response, request
from database.models import Brevet
from flask_restful import Resource
import dateutil.parser


class BrevetsAPI(Resource):
    def get(self):
        brevets = Brevet.objects().to_json()
        return Response(brevets, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        brevet = Brevet(**body).save()
        id = brevet.id
        return {'id': str(id)}, 200