from flask import Flask, Response, render_template, send_from_directory
from flask import session, redirect, url_for, escape, request
from flask_socketio import SocketIO
from hashlib import md5
import json
import MySQLdb

socketio = SocketIO()


def create_app(debug=False):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.debug = debug
    app.config["SECRET_KEY"] = 'strong secret'

    from modules.rainmachine.controller import rainmachine_mod as rainmachine_module
    from modules.purpleair.controller import purpleair_mod as purpleair_module
    from modules.wago.controller import wago_mod as wago_module
    from modules.camera.controller import camera_mod as camera_module

    app.register_blueprint(rainmachine_module)
    app.register_blueprint(purpleair_module)
    app.register_blueprint(wago_module)
    app.register_blueprint(camera_module)

    db = MySQLdb.connect(host="localhost", user="admin", passwd="strong password", db="capstone")
    cur = db.cursor()

    import jinja2.exceptions

    class ServerError(Exception):pass

    with app.app_context():
        @app.route('/')
        def index():
            if 'username' in session:
                return redirect(url_for('login'))

            username_session = escape(session['username']).capitalize()
            return render_template('index.html', session_user_name=username_session)

        @app.route('/login', methods=['GET', 'POST'])
        def login():
            if 'username' in session:
                return redirect(url_for('index'))

            error = None
            try:
                if request.method == 'POST':
                    username_form  = request.form['username']
                    cur.execute("SELECT COUNT(1) FROM users WHERE name = {};"
                            .format(username_form))

                if not cur.fetchone()[0]:
                    raise ServerError('Invalid username')
                    password_form  = request.form['password']
                    cur.execute("SELECT pass FROM users WHERE name = {};"
                            .format(username_form))

                for row in cur.fetchall():
                    if md5(password_form).hexdigest() == row[0]:
                        session['username'] = request.form['username']
                    return redirect(url_for('index'))

                raise ServerError('Invalid password')
            except ServerError as e:
                error = str(e)
            return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect(url_for('index'))

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
