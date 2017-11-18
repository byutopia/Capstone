from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

#create the home template you can set prefix with url_prefix ='/prefix'
rainmachine_mod = Blueprint('rainmachine', __name__)
#set a route
@rainmachine_mod.route('/rainmachine', methods = ['GET'])
def rainmachine():
	#return the template
	return render_template("rainmachine.html")
