import requests
import json
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from ... import socketio
from ... import _config

from API import API

api = API()

# create the home template you can set prefix with url_prefix ='/prefix'
rainmachine_mod = Blueprint('rainmachine', __name__)
# set a route
# This function gets the information from the Rainmachine API and adds it to an array to be sent to the Rainmachine Template.
# It gets the information about the Programs, Zones, Zone Properties, and Weather Mixer.
# That is all put in an array called data, then when the page it rendered the information can be accessed using the variable rainmachineInfo.name from this page.info you want to acces
def get_all():
    data ={}
    if api.init['error'] != 0:
        return api.init['message']
    try:
        req = api.get("program") # get program information
        if req['error'] != 0:
            return req['message']
        else:
            data['program'] = req['result']

        req = api.get("zone")# get zone information
        if req['error'] != 0:
            return req['message']
        else:
            data['zone'] = req['result']

        req = api.get("zone/properties") # get zone properties
        if req['error'] != 0:
            return req['message']
        else:
            data['properties'] = req['result']

        req = api.get("mixer")# get weather mixer information
        if req['error'] != 0:
            return req['message']
        else:
            data['mixer'] = req['result']
            return data
            #return render_template("rainmachine.html", rainmachineInfo = data)
    except ValueError:
        return "Error reading API response"

# send updated rainmachine data on page change
@socketio.on('getData') 
def send_data():
    data = get_all()
    if type(data) == dict:
        socketio.emit('rainmachineData', data)

# return main Ui page
@rainmachine_mod.route('/rainmachine', methods = ['GET'])
def rainmachine():
    # prevents people who are not logged in to type in URL directly
    if 'username' not in session:
        return redirect(url_for('login'))
    #must have rainmachine in their roles in order access this page
    if 'rainmachine' not in session['roles']:
        return redirect(url_for('index'))
    data = get_all()
    if type(data) == dict:
        data['weather'] = _config['rainmachine']['weather']
        return render_template("rainmachine.html", rainmachineInfo = {'success': 1, 'data': data})
    else: 
        return render_template("rainmachine.html", rainmachineInfo = {'success': 0, 'data': "Error reading API response"})

@rainmachine_mod.route('/rainmachine/zstart', methods = ['POST']) # POST to start zone 
def zstart():
    data = '{"time": 300}' # have to send the amount of time you want the zone to run, we defualt to 5 mins
    zoneID = request.get_json()["id"]# gets id from rainmachine template button
    req = api.post("zone/{zoneID}/start".format(zoneID=zoneID), data) # actual post request
    print req
    if req:#['error'] != 0:
        socketio.emit('rainmachineUpdate', {'type': 'zone', 'data': {'zoneID': zoneID, 'status': 'started', 'time': 300}})
        return json.dumps({'status': "ok"})
    else:
        return json.dumps({'status': "failed"})

@rainmachine_mod.route('/rainmachine/zstop', methods = ['POST'])# POST to stop zone
def zstop():
    zoneID = request.get_json()["id"]# gets id from rainmachine template
    if api.post("zone/{zoneID}/stop".format(zoneID=zoneID)):# acutaly POST request
        # if req['error'] != 0:
        socketio.emit('rainmachineUpdate', {'type': 'zone', 'data': {'zoneID': zoneID, 'status': 'stopped'}})
        return json.dumps({'status': "ok"})
    else:
        return json.dumps({'status': "failed"})

@rainmachine_mod.route('/rainmachine/pstart', methods = ['POST'])# POST to start program
def pstart():
    data = '{"time": 300}'
    programID = request.get_json()["id"]# gets id from rainmachine template
    req = api.post("program/{programID}/start".format(programID=programID), data)# acutaly POST request
    if req:#['error'] != 0:
        socketio.emit('rainmachineUpdate', {'type': 'program', 'data': {'programID': programID, 'status': 'started', 'time': 300}})
        return json.dumps({'status': "ok"})
    else:
        return json.dumps({'status': "failed"})

@rainmachine_mod.route('/rainmachine/pstop', methods = ['POST'])# POST to stop program
def pstop():
    programID = request.get_json()["id"]# gets id from rainmachine template
    if api.post("program/{programID}/stop".format(programID=programID)):# acutaly POST request
        # if req['error'] != 0:
        socketio.emit('rainmachineUpdate', {'type': 'program', 'data': {'programID': programID, 'status': 'stopped'}})
        return json.dumps({'status': "ok"})
    else:
        return json.dumps({'status': "failed"})
