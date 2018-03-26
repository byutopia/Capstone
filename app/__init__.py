from flask import Flask, Response, render_template, send_from_directory, flash
from flask import session, redirect, url_for, escape, request
from flask_socketio import SocketIO
from hashlib import md5
import json

import includes.config as _config
import includes.db as _db

socketio = SocketIO()
DB = _db.DBC()

def create_app(debug=False):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.debug = debug
    app.config["SECRET_KEY"] = _config.app['secret_key']

    from modules.rainmachine.controller import rainmachine_mod as rainmachine_module
    from modules.purpleair.controller import purpleair_mod as purpleair_module
    from modules.wago.controller import wago_mod as wago_module
    from modules.camera.controller import camera_mod as camera_module

    app.register_blueprint(rainmachine_module)
    app.register_blueprint(purpleair_module)
    app.register_blueprint(wago_module)
    app.register_blueprint(camera_module)

    class ServerError(Exception):pass

    import jinja2.exceptions

    @app.route('/')
    def index():
        # If there isn't a logged on session, force them to login.
            if 'username' not in session:
                return redirect(url_for('login'))
        # If someone tries to inject HTML into the session variable, reset it to the default. 
            if 'username' in session:
                username_session = escape(session['username']).capitalize()
                return render_template('index.html', session_user_name=username_session)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if 'username' in session:
            return redirect(url_for('index'))
            print 'No error'
        try:
            # Look for a form to grab a username from (this form is in the login.html file).
            # Grab the username and password and check it against the database. 
            # For the password, checked the hashed data in the database against the plaintext entered. 
            # Take the information and also create a new session that assigns permissions to the user. 
            if request.method == 'POST':
                username_form = request.form['username']
                password_form = request.form['password']
                check = DB.loginCheck(username_form, password_form)
                if check['status'] == 0:
                    session['username'] = username_form
                    # session variable for Display name
                    session['firstname'] = check['data']['firstname']
                    # session variable for role based access
                    session['roles'] = check['data']['roles']
                    # redirect to main page
                    return redirect(url_for('index'))
                # throws errors if not all fields in login are filled out
                elif check['status'] == 1:
                    flash(u'Missing Credentials', 'error')
                # throws error if invalid credentials for login
                elif check['status'] == 2:
                    flash(u'Invalid Credentials', 'error')
                elif check['status'] == -1:
                    flash(check['message'], 'error')
                else:
                    flash(u'Server error', 'error')
                
        except:
            import sys
            return "I'm broken you hurt me :(\n %s" % sys.exc_info()[1]
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        # Upon logout, destroy all active sessions.
        session.pop('username', None)
        session.pop('roles', None)
        session.pop('firstname', None)
        session.clear()
        print 'Cleared'
        return redirect(url_for('login'))

    @app.route('/<pagename>')
    def admin(pagename):
        return render_template(pagename+'.html')

    @app.route('/<path:resource>')
    def serve_static_resource(resource):
        return send_from_directory(app.static_folder, resource)

    @app.route('/teapot')
    def teapot():
        return Response(json.dumps({'message': 'I am a teapot!'}), status=418, mimetype='application/json')

    @app.errorhandler(jinja2.exceptions.TemplateNotFound)
    def template_not_found(e):
        return not_found(e)

    @app.errorhandler(404)
    def not_found(e):
        return '<strong>Page Not Found!</strong>', 404

    socketio.init_app(app)
    return app
