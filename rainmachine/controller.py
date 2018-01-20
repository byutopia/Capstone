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
        req = api.get("zone")
        if req['error'] != 0:
            return req['message']
        else:
            res = req['result']
            # return the template
            return render_template("rainmachine.html", zones=res['zones'])
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
