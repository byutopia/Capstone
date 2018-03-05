from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

purpleair_mod = Blueprint('purpleair', __name__)
#set a route
purpleairDevices = [{'ip':"192.168.20.61", 'lat':40.315155, 'lon':-111.666672 },{'ip':'192.168.20.59','lat':40.324207,'lon':	-111.715004}]
@purpleair_mod.route('/purpleair', methods = ['GET'])
def purpleair():
	#return the template
	return render_template("purpleair.html", devices = purpleairDevices)
