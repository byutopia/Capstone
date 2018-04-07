from flask import Blueprint, request, render_template, session, redirect
from ... import socketio

wago_mod = Blueprint('wago', __name__)
wago_hit = False

#socketio = SocketIO()
@socketio.on('getWago')
def sendWagoStatus():
    socketio.emit('wagoUpdate', wago_hit)

# set route
@wago_mod.route('/wago', methods = ['GET', 'POST'])
def wago():
    global wago_hit
    
    if request.method == 'POST':
        wago_hit = not wago_hit # flip boolean for whether Wago is in an on state or off state
        socketio.emit('wagoUpdate', {'lightsOn': wago_hit}) # update page when boolean flips
        return 'ok'

    else:
        # prevents someone who is not logged in from getting access by typing the URL
        if 'username' not in session:
            return redirect(url_for('login'))
        # checks for wago access in roles, otherwise directs to index
        if 'wago' not in session['roles']:
            return redirect(url_for('index'))

        return render_template("wago.html", data={'status': wago_hit}) # return main UI

