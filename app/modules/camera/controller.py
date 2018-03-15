from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

camera_mod = Blueprint('camera', __name__)
#set a route
@camera_mod.route('/camera', methods = ['GET'])
def camera():
    if 'username' not in session:
        return redirect(url_for('login'))
    if 'camera' not in session['roles']:
        return redirect(url_for('index'))
    #return the template
    return render_template("camera.html")
