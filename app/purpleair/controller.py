from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

purpleair_mod = Blueprint('purpleair',__name__)

@purpleair_mod.route('/purpleair',methods=['GET'])
def purpleair()
	return render_template("purpleair.html")