"""
Nose tests for mongodb connection
"""

import flask
from flask import request
import arrow
from flask_brevets import app

import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


def t_insert(item):
    with app.test_request_context(path="/_insert", method="POST", json=item):
        rt = flask.make_response(app.dispatch_request())
        log.debug(f"status={rt.status_code}")
        return rt


def t_fetch():
    with app.test_request_context("/_fetch"):
        rt = flask.make_response(app.dispatch_request()).json
        #log.debug(f"json={rt}")
        return rt

# def test_fetch_empty():
    # assert t_fetch() == None

def test_insert_fetch():
    test_doc = {
        'brevet_dist_km': 200,
        'begin_date': "2022-02-03T09:00",
        'table': [ { 'km': 100.0, 'location': "", 'open_time': "2022-02-03T11:56", 'close_time': "2022-02-03T15:40" } ]
    }
    
    #log.debug(str(test_doc['table']))
    
    assert t_insert(test_doc).status_code == 200
    f = t_fetch()
    log.debug(f"Received: {f}")
    log.debug(f"Expected: {test_doc}")
    assert f == test_doc


def test_insert_empty():
    test_doc = {
        'brevet_dist_km': 200,
        'begin_date': arrow.now().format(),
        'table': [ { 'km': None, 'location': "", 'open_time': "", 'close_time': "" } for x in range(19) ]
    }
    
    rs = t_insert(test_doc)
    e = rs.json
    assert "Empty table" in e['error']
    assert rs.status_code == 400
    assert t_fetch() != None

def test_insert_incomplete():
    test_doc = {
        'brevet_dist_km': 200,
        'table': [ { 'km': None, 'location': "", 'open_time': "", 'close_time': "" } for x in range(19) ]
    }
    
    rs = t_insert(test_doc)
    e = rs.json
    log.debug(f"Received: {e}")
    assert "Data does not contain expected keys" in e['error']
    assert rs.status_code == 400