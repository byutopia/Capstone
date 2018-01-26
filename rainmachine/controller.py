import requests
import json
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from API import API
from datetime import datetime
api = API()

# create the home template you can set prefix with url_prefix ='/prefix'
rainmachine_mod = Blueprint('rainmachine', __name__)
# set a route
@rainmachine_mod.route('/rainmachine', methods = ['GET'])
def rainmachine():
    if api.init['error'] != 0:
        return api.init['message']
    try:
        #req = api.get("program")
        data ={}
        req = api.get("program")
        if req['error'] != 0:
            return req['message']
        else:
            data['program'] = req['result']

        req = api.get("zone")
        if req['error'] != 0:
            return req['message']
        else:
            data['zone'] = req['result']

        req = api.get("zone/properties")
        if req['error'] != 0:
            return req['message']
        else:
            data['properties'] = req['result']

        req = api.get("mixer")
        if req['error'] != 0:
            return req['message']
        else:
            data['mixer'] = req['result']
            return render_template("rainmachine.html", rainmachineInfo = data)
    except ValueError:
        return "Error reading API response"

@rainmachine_mod.route('/rainmachine/start', methods = ['POST'])
def start():
    data = '{"time": 300}'
    zoneID = request.get_json()["id"]
    req = api.post("zone/{zoneID}/start".format(zoneID=zoneID), data)
    print req
    if req:#['error'] != 0:
        return json.dumps({'status': "ok"})
    else:
        return json.dumps({'status': "failed"})

@rainmachine_mod.route('/rainmachine/stop', methods = ['POST'])
def stop():
    zoneID = request.get_json()["id"]
    if api.post("zone/{zoneID}/stop".format(zoneID=zoneID)):
        # if req['error'] != 0:
        return json.dumps({'status': "ok"})
    else:
        return json.dumps({'status': "failed"})


@rainmachine_mod.route('/rainmachine/diag', methods = ['GET'])
# get diagnostic info
def diag():
    if api.init['error'] != 0:
       return api.init['message']
    try:
        req = api.get("api/4/diag")
        if req['error'] != 0:
            return req['message']
        else:
            return res['result']
    except ValueError:
        return "Error reading API response"
