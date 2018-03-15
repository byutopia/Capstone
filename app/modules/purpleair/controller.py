from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
import requests
purpleair_mod = Blueprint('purpleair', __name__)
#set a route
purpleairIPs = ['192.168.20.61','192.168.20.59']

ses = requests.Session()

def getCordsByIP(IPs):
	cordsAndIP = []
	URL = "http://{}/json"
	for ip in IPs:
		try:
			url = URL.format(ip)
			req = ses.get(url, timeout=3, verify=False)
			res = req.json()
			lat = res['lat']
			lon = res['lon']
			cordsAndIP.append({'ip':ip,'lat':lat, 'lon': lon})
		except ValueError:
			return{"error": 2, "message": "Error reading received JSON object"}
		except requests.exceptions.RequestException:
			print "Error: could not connect to IP "
			print ip
	return cordsAndIP

purpleairDevices = getCordsByIP(purpleairIPs)
print purpleairDevices
@purpleair_mod.route('/purpleair', methods = ['GET'])
def purpleair():
    if 'username' not in session:
        return redirect(url_for('login'))
    if 'purpleair' not in session['roles']:
        return redirect(url_for('index'))
    #return the template
    return render_template("purpleair.html", devices = purpleairDevices)
