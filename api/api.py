"""
Brevets RESTful API
"""

import os
from flask import Flask
from flask_restful import Resource, Api
from mongoengine import connect
from resources import BrevetAPI, BrevetsAPI

app = Flask(__name__)
api = Api(app)
connect(db='brevets_db', host="mongodb://" + os.environ['MONGODB_HOSTNAME'], port=int(os.environ['MONGODB_PORT']))

##
# API Resource Routing
##
api.add_resource(BrevetsAPI, '/api/brevets')
api.add_resource(BrevetAPI, '/api/brevet/<id>')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'], debug=os.environ['DEBUG'])