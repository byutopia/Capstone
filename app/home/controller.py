from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

#create the home template you can set prefix with url_prefix ='/prefix'
home_mod = Blueprint('home', __name__)
#set a route
@home_mod.route('/', methods = ['GET'])
def home():
	#return the template
	return render_template("index.html")