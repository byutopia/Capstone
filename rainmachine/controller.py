import requests
import json
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from API import API

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
