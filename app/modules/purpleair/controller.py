from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import requests
from ... import _config
purpleair_mod = Blueprint('purpleair', __name__)
#the ips to get for each device
purpleairIPs = _config.purpleair['addresses']

ses = requests.Session()

def getCordsByIP(IPs):
	cordsAndIP = {}
	URL = "http://{}/json"
	#get lat and lon by ip
	for ip in IPs:
		try:
			#make the url string to request with
			url = URL.format(ip)
			#make a request for the purple air data
			req = ses.get(url, timeout=3, verify=False)

			res = req.json()
			lat = res['lat']
			lon = res['lon']
			#make the object to pass to the template
			cordsAndIP.append({'ip':ip,'lat':lat, 'lon': lon})
		except ValueError:
			return{"error": 2, "message": "Error reading received JSON object"}
		except requests.exceptions.RequestException as e:
			print e
	return cordsAndIP

purpleairDevices = getCordsByIP(purpleairIPs)
@purpleair_mod.route('/purpleair', methods = ['GET'])
def purpleair():
    # check the user credentials
    if 'username' not in session:
        return redirect(url_for('login'))
    # checks for purpleair access in roles
    if 'purpleair' not in session['roles']:
        return redirect(url_for('index'))
    #return the template with device data
    return render_template("purpleair.html", devices = purpleairDevices)
