"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import os
import flask
from flask import request
from werkzeug.exceptions import BadRequest
import requests
from bson import json_util

import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations

import logging

###
# Globals
###

app = flask.Flask(__name__)

AURL = "http://" + os.environ['API_ADDR'] + ":" + os.environ['API_PORT']
AURL_BREVETS = AURL + "/api/brevets"
AURL_BREVET = AURL + "/api/brevet/"


###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects: number of kilometers, brevet distance, date and time of start.
    """
    app.logger.debug("Got a JSON GET request")
    km = request.args.get('km', 999, type=float)
    app.logger.debug("km={}".format(km))
    br = request.args.get('brevet_dist_km', 200, type=int)
    app.logger.debug(f"brevet={br}")
    begin = request.args.get('begin_date', "2021-01-01T00:00", type=str)
    app.logger.debug(f"begin={begin}")
    app.logger.debug("request.args: {}".format(request.args))

    try:
        open_time = acp_times.open_time(km, br, arrow.get(begin)).format('YYYY-MM-DDTHH:mm')
        close_time = acp_times.close_time(km, br, arrow.get(begin)).format('YYYY-MM-DDTHH:mm')
    except ParserError as p:
        app.logger.debug(f"Error: {p}")
        return flask.jsonify(error=str(p)), 400
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


@app.route("/_insert", methods=['POST'])
def _insert():

    app.logger.debug("Got a JSON POST request")
    
    # Check if valid json
    try:
        data = request.json
        if not all(x in data.keys() for x in ['brevet_dist_km', 'begin_date', 'table']):
            raise BadRequest("Data does not contain expected keys")
        if not any((x['km'] != None) for x in data['table']):
            raise BadRequest("Empty table")
    except BadRequest as exc:
        app.logger.debug(f"Exception: {exc}")
        return flask.jsonify(error=str(exc)), 400

    d = request.json
    ln = len(d['table'])
    for x in range(ln):
        if d['table'][ln-1-x]['km'] == None:
            del d['table'][ln-1-x]
    
    r = {
        'length': d['brevet_dist_km'],
        'start_time': d['begin_date'],
        'checkpoints': [ {'distance': x['km'], 'location': x['location'], 
                'open_time': x['open_time'], 'close_time': x['close_time']} for x in d['table'] ]
    }
    app.logger.debug(f"Sending as json: {str(r)}")
    
    req = requests.post(AURL_BREVETS, json=r)
    
    #app.logger.debug(f"Response text: {req.text}")
    
    return flask.jsonify(success=True)


@app.route("/_fetch")
def _fetch():
    app.logger.debug("Got a fetch request")
    
    try:
        rs = requests.get(AURL_BREVETS)
        brs = json_util.loads(rs.content)
        #app.logger.debug(f"Got brevets: {str(brs)}")
        #app.logger.debug(f"type: {type(brs)}")
        br = brs[len(brs)-1]
        br.pop('_id')
        br['start_time'] = str(arrow.get(br['start_time']).format('YYYY-MM-DDTHH:mm'))
        for x in br['checkpoints']:
            for y in ['open_time', 'close_time']:
                x[y] = str(arrow.get(x[y]).format('YYYY-MM-DDTHH:mm'))
        #app.logger.debug(f"Got last: {str(br)}")
    except Exception as e:
        app.logger.debug(f"Exception: {e}")
        return flask.jsonify(error=str(e))
    
    rt = {
        'brevet_dist_km': int(br['length']),
        'begin_date': br['start_time'],
        'table': [ {'km': x['distance'], 'location': x['location'], 
                'open_time': x['open_time'], 'close_time': x['close_time']} for x in br['checkpoints']]
    }
    #app.logger.debug(f"Returning as json: {str(rt)}")
    
    return flask.jsonify(rt)
    

#############

app.debug = os.environ['DEBUG']
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(os.environ['PORT']))
    app.run(port=os.environ['PORT'], host="0.0.0.0")
