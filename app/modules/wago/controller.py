from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from ... import socketio

wago_mod = Blueprint('wago', __name__)
wago_hit = False

#socketio = SocketIO()

# set route
@wago_mod.route('/wago', methods = ['GET', 'POST'])
def wago():
    global wago_hit

    if request.method == 'POST':
        wago_hit = not wago_hit
        socketio.emit('wagoUpdate', {'lightsOn': wago_hit})
        return 'ok'
    else:
        return render_template("wago.html", data={'status': wago_hit})
